# -*- coding: utf-8 -*-
from collections import defaultdict
#from odoo.addons.hr_payroll.wizard.hr_payroll_payslips_by_employees import HrPayslipEmployees
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import format_date
import logging
_logger = logging.getLogger(__name__)

class HrPayslipEmployeesExt(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    
    def compute_sheet(self):
        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            today = fields.date.today()
            first_day = today + relativedelta(day=1)
            last_day = today + relativedelta(day=31)
            if from_date == first_day and end_date == last_day:
                batch_name = from_date.strftime('%B %Y')
            else:
                batch_name = _('From %s to %s', format_date(self.env, from_date), format_date(self.env, end_date))
            payslip_run = self.env['hr.payslip.run'].create({
                'name': batch_name,
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        employees = self.with_context(active_test=False).employee_ids
        if not employees:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))

        #Prevent a payslip_run from having multiple payslips for the same employee
        employees -= payslip_run.slip_ids.employee_id
        success_result = {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.run',
            'views': [[False, 'form']],
            'res_id': payslip_run.id,
        }
        if not employees:
            return success_result

        payslips = self.env['hr.payslip']
        Payslip = self.env['hr.payslip']

        contracts = employees._get_contracts(payslip_run.date_start, payslip_run.date_end, states=['open']).filtered(lambda c: c.active)
        #raise UserError(contracts)
        date_from = datetime(payslip_run.date_start.year, payslip_run.date_start.month, payslip_run.date_start.day)
        date_to = datetime(payslip_run.date_end.year, payslip_run.date_end.month, payslip_run.date_end.day)
        contracts._generate_work_entries(date_from, date_to)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', employees.ids),
        ])
        
        # self._check_undefined_slots(work_entries, payslip_run)
        # payslip_work_entries._check_undefined_slots(slip.date_from, slip.date_to)

        if(self.structure_id.type_id.default_struct_id == self.structure_id):
            work_entries = work_entries.filtered(lambda work_entry: work_entry.state != 'validated')
            if work_entries._check_if_error():
                work_entries_by_contract = defaultdict(lambda: self.env['hr.work.entry'])

                for work_entry in work_entries.filtered(lambda w: w.state == 'conflict'):
                    work_entries_by_contract[work_entry.contract_id] |= work_entry

                for contract, work_entries in work_entries_by_contract.items():
                    conflicts = work_entries._to_intervals()
                    time_intervals_str = "\n - ".join(['', *["%s -> %s" % (s[0], s[1]) for s in conflicts._items]])
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Some work entries could not be validated.'),
                        'message': _('Time intervals to look for:%s', time_intervals_str),
                        'sticky': False,
                    }
                }


        default_values = Payslip.default_get(Payslip.fields_get())
        #if not self.structure_id or self.structure_id.name == 'Ordinaria Quincenal':        
        #raise UserError(str(days))
        #days = (0,0,{
        #    'work_entry_type_id': 1,
        #    'name': 'WORK100',
        #    'number_of_days': 365,
        #    'number_of_hours': 121.68,
        #})

        payslips_vals = []
        for contract in self._filter_contracts(contracts):
            values = dict(default_values, **{
                'name': _('New Payslip'),
                'employee_id': contract.employee_id.id,
                #'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': self.structure_id.id or contract.structure_type_id.default_struct_id.id,
                #Add
                'worked_days_line_ids': self.env['hr.payslip'].get_worked_day_lines(self._filter_contracts(contract),payslip_run.date_start,payslip_run.date_end),
                'tipo_nomina' : payslip_run.tipo_nomina,
                'fecha_pago' : payslip_run.fecha_pago,
                'journal_id': payslip_run.journal_id.id,
                'dias_pagar': payslip_run.dias_pagar,
                'imss_dias': payslip_run.imss_dias,
                'imss_mes': payslip_run.imss_mes,
                'no_nomina': payslip_run.no_nomina,
                'mes': '{:02d}'.format(payslip_run.date_end.month),
                'isr_devolver': payslip_run.isr_devolver,
                'isr_ajustar': payslip_run.isr_ajustar,
                'concepto_periodico': payslip_run.concepto_periodico,
            })
            payslips_vals.append(values)
        #raise UserError(payslips_vals)
        payslips = Payslip.with_context(tracking_disable=True).create(payslips_vals)
        payslips._compute_name()
        for r in payslips:
            r.compute_sheet()
        payslip_run.state = 'verify'

        return success_result