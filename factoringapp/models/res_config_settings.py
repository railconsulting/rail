from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']
    
    bizylife_factoring_partner_id = fields.Many2one(comodel_name="res.partner", 
                                                    related='company_id.bizylife_factoring_partner_id', 
                                                    string="Factoring Partner ID",
                                                    readonly=False,
                                                    check_company=True,
                                                    )
    
    bizylife_default_factoring_liability_account_id = fields.Many2one(comodel_name="account.account", 
                                                                    related='company_id.bizylife_default_factoring_liability_account_id',
                                                                    string="Default Factoring Liability Account", 
                                                                    help="Default",
                                                                    readonly=False,
                                                                    check_company=True,
                                                                    )
class ResCompany(models.Model):
    _inherit = "res.company"

    bizylife_factoring_partner_id = fields.Many2one(comodel_name="res.partner")
    bizylife_default_factoring_liability_account_id = fields.Many2one(comodel_name="account.account", 
                                                                    string="Liability Account", 
                                                                    )
    