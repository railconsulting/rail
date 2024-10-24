# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class HrHolidaysStatus(models.Model):
    _inherit = 'hr.leave.type'

    limit = fields.Boolean()
    
    def unlink(self):
        auto_created_leaves = []
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_fjc', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_fjs', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_fi', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_vac', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_fr', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_inc_mat', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_inc_eg', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_inc_rt', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_dfest', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        leave_type = self.env.ref('nomina_cfdi_extras.hr_holidays_status_dfest3', False)
        if leave_type:
            auto_created_leaves.append(leave_type.id)
        for status in self:
            if status.id in auto_created_leaves:
                raise UserError("No puedes borrar un registro creado automáticamente %s"%(status.name))
