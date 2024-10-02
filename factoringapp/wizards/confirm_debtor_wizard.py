import requests,json
from datetime import date,timedelta
from odoo import models,fields,exceptions

class ConfirmDebtorWizard(models.TransientModel):
    _name = 'bizylife.confirmdebtorwizard'
    
    yes_no = fields.Char(default='This debtor has not yet been approved for factoring with AR Funding.  Do you want to send this debtor to AR Funding for approval?')

    def yes(self):
        print('context',self._context,self._context.get('related_invoice'),self._context.get('active_id'))
        related_invoice = self.env['account.move'].search([('id','=',self._context.get('related_invoice'))]) if self._context.get('related_invoice') else None
        partner_id = related_invoice.partner_id if related_invoice else self.env['res.partner'].search([('id','=',self._context.get('active_id'))])
        print('related invoice:',related_invoice,'partner id:',partner_id)
        if(not partner_id.vat):
            raise exceptions.ValidationError("You need to set the tax id for this debtor before submitting it for approval.")

        start_date = date(date.today().year-1,1,1)
        end_date = date(date.today().year-1,12,31)
        print(start_date,'-',end_date)
        partner_invoices = self.env['account.move'].search(['&','&',('partner_id','=',partner_id.id),('invoice_date','>=',start_date),('invoice_date','<=',end_date)])
        print(partner_invoices)
        avg_monthly_invoicing = 0
        for invoice in partner_invoices:
            avg_monthly_invoicing += invoice.amount_total
        print(avg_monthly_invoicing)
        url = 'https://arfunding.odoo.com/debtors/update'
        obj = {
            "customer":self.env.company.name,
            "name":partner_id.name, 
            "email":partner_id.email,
            "customer_taxid":self.env.company.vat,
            "debtor_taxid":partner_id.vat,
            "avg_monthly_invoicing": avg_monthly_invoicing/12,
        }
        res = requests.post(url,json=obj)
        if(res.status_code == 200):
            json_res = json.loads(res.content)['result']
            if (json_res['code'] == 200 and json_res['status'] == 'Created Debtor Request'):
                partner_id.bizylife_debtor_approval_status = 'pending'
            else:
                raise exceptions.ValidationError(str(json_res['code']) + ' ' + json_res['status'] + ': ' + json_res['description'])

    def no(self):
        return False
    
    