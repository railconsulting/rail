import requests,json
from datetime import date,timedelta
from odoo import models,fields,exceptions

class ApprovedMessage(models.TransientModel):
    _name = 'bizylife.approvedmessagewizard'
    
    dialog_message = fields.Text(default="""    
    Great news! Based on your responses, you pre-qualify for our working capital program through the Odoo integration.
    What’s Next?

    1) Personalized Follow-Up: A representative from AR Funding will contact you shortly to review your information 
       and answer any questions you may have.
    2) Application & Approval Process: We will guide you through our straightforward application and approval process, 
       ensuring everything is set up smoothly.
    3) Start Submitting Invoices: Once approved, you’ll be ready to start submitting invoices through the integration 
       and accessing immediate working capital.
                                 
    We’re excited to help you unlock cash flow and support your business growth.              
    If you have any immediate questions, feel free to reach out to our team at 800-756-3386.
                                 """)
    
    def okay(self):
        return