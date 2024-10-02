from odoo import models,fields

class Partner(models.Model):
    _inherit = 'res.partner'
    bizylife_customer_approval_status = fields.Selection([('approved','Approved'),('pending','Pending Approval'),('rejected','Rejected')],string="Customer Approval Status")
    bizylife_debtor_approval_status = fields.Selection([('approved','Approved'),('pending','Pending Approval'),('rejected','Rejected')],string="Debtor Approval Status")
    bizylife_rejection_reason = fields.Char(string="Rejection Reason")
    
    def send_debtor_for_approval(self):
        print('sending debtor for approval')          
        return {
        'name': 'Debtor not yet approved',
        'type': 'ir.actions.act_window',
        'res_model': 'bizylife.confirmdebtorwizard',
        'view_mode': 'form',
        'view_type': 'form',
        'context': {},
        'target': 'new',
        }