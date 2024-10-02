import requests,json
from datetime import date,timedelta
from odoo import models,fields,exceptions

class WelcomeMessage(models.TransientModel):
    _name = 'bizylife.welcomemessagewizard'
    
    dialog_message = fields.Text(default="""    
    Thank you for choosing AR Funding! We’re excited to help you unlock instant working capital directly within your Odoo ERP system.
        
    Our seamless integration offers you:

        - Immediate Access to Cash: Convert your invoices into working capital instantly.
        - Streamlined Financial Operations: Enjoy a user-friendly, automated process that fits perfectly into your existing Odoo setup.
        - Enhanced Cash Flow Management: Improve your financial stability with a reliable and efficient solution.
        
    Welcome aboard, and we look forward to helping you succeed

    We’re here to support your business growth every step of the way. If you have any questions or need assistance, you can contact 
    us directly at 800-756-3386.

    Sincerely,
    AR Funding Team
                                 """)
    
    def redirect_questionnaire(self):
        print('redirecting to questionnaire')
        return {
            'name': 'Unlock Instant Working Capital with Odoo Integration',
            'type': 'ir.actions.act_window',
            'res_model': 'questionnaire.wizard.question',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': {},
            'target': 'current',
        }
        