# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

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
        ##self._post_payments(to_process, edit_mode=edit_mode)
        ##self._reconcile_payments(to_process, edit_mode=edit_mode)
        return payments
