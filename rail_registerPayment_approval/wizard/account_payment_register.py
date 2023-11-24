# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def _request_approval(self):
        '''
        1. create request
        2. Submit request
        3. update x_has_request_approval = True
        4. open request form view
        '''
        self.ensure_one()

        if not self.type_id.active or not self.type_id.is_configured or \
                not self.origin_ref.x_need_approval:
            raise UserError(
                _('Data is changed! Please refresh your browser in order to continue !'))
        if self.origin_ref.x_has_request_approval and \
                not self.type_id.is_free_create:
            raise UserError(
                _('Request has been created before !'))
        
        # create request
        vals = {
            'name': self.name,
            'priority': self.priority,
            'type_id': self.type_id.id,
            'description': self.description,
            'origin_ref': '{model},{res_id}'.format(
                model=self.origin_ref._name,
                res_id=self.origin_ref.id)
        }
        request = self.env['multi.approval'].create(vals)
        request.action_submit()

        # update x_has_request_approval
        self.env['multi.approval.type'].update_x_field(
            request.origin_ref, 'x_has_request_approval')

        return {
            'name': _('My Requests'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi.approval',
            'res_id': request.id,
        }
    
    def _create_payments(self):
        self.ensure_one()
        all_batches = self._get_batches()
        batches = []
        # Skip batches that are not valid (bank account not trusted but required)
        for batch in all_batches:
            batch_account = self._get_batch_account(batch)
            if self.require_partner_bank_account and not batch_account.allow_out_payment:
                continue
            batches.append(batch)

        if not batches:
            raise UserError(_('To record payments with %s, the recipient bank account must be manually validated. You should go on the partner bank account in order to validate it.', self.payment_method_line_id.name))

        first_batch_result = batches[0]
        edit_mode = self.can_edit_wizard and (len(first_batch_result['lines']) == 1 or self.group_payment)
        to_process = []

        if edit_mode:
            payment_vals = self._create_payment_vals_from_wizard(first_batch_result)
            to_process.append({
                'create_vals': payment_vals,
                'to_reconcile': first_batch_result['lines'],
                'batch': first_batch_result,
            })
        else:
            # Don't group payments: Create one batch per move.
            if not self.group_payment:
                new_batches = []
                for batch_result in batches:
                    for line in batch_result['lines']:
                        new_batches.append({
                            **batch_result,
                            'payment_values': {
                                **batch_result['payment_values'],
                                'payment_type': 'inbound' if line.balance > 0 else 'outbound'
                            },
                            'lines': line,
                        })
                batches = new_batches

            for batch_result in batches:
                to_process.append({
                    'create_vals': self._create_payment_vals_from_batch(batch_result),
                    'to_reconcile': batch_result['lines'],
                    'batch': batch_result,
                })

        payments = self._init_payments(to_process, edit_mode=edit_mode)
        self._request_approval()
        self._post_payments(to_process, edit_mode=edit_mode)
        self._reconcile_payments(to_process, edit_mode=edit_mode)
        return payments
