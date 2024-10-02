import requests,json
from odoo import models,exceptions,fields

class Company(models.Model):
    _inherit = 'res.company'
    bizylife_customer_approval_status = fields.Selection([('approved','Approved'),('pending','Pending Approval'),('rejected','Rejected')],string="Customer Approval Status")
    bizylife_factoring_customer_id = fields.Char(string="Factoring Customer ID")