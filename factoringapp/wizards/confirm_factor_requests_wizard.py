import requests,json,base64
from datetime import date,timedelta
from odoo import models,fields,exceptions

class ConfirmFactorRequests(models.TransientModel):
    _name = 'bizylife.confirmfactorrequests'

    dialog = fields.Char()
    confirm_message = fields.Char(default='For value received, we hereby assign and transfer the invoices and its proceeds to'+
                           ' Associated Receivables Funding, Inc., who is the owner of this invoice unencumbered by any other security or'+
                           ' claims pursuant to the master agreement. The undersigned does herewith assign all lien rights, choses in action,'+
                           ' chattel paper or contract rights. We further certify that the goods have been shipped and/or services performed'+
                           ' in agreement with all terms and conditions.')

    def _show_invoices(self):
        for record in self:
            print('hello there')
            print(self._context)
            # invoices = self._context.get('active_ids')
            # for invoice in invoices:
            #     record = self.env['account.move'].search([('id','=',invoice)])
            record.dialog = "hello there"
    
    def confirm(self):
        print(self._context)
        invoices = self._context.get('active_ids')
        for invoice in invoices:
            record = self.env['account.move'].search([('id','=',invoice)])
            sale_order = self.env['sale.order'].search([('name','=',record.invoice_origin)])
            invoice_pdf = self.env['ir.actions.report']._render('account.account_invoices', [record.id])[0]
            picking_ids = filter(lambda picking_id : picking_id.location_dest_id.usage == "customer" and picking_id.state == 'done', sale_order.picking_ids)
            tracking_number_string = None
            for picking_id in picking_ids:
                if hasattr(picking_id,'carrier_tracking_ref'):
                    if tracking_number_string == None:
                        tracking_number_string = picking_id.carrier_tracking_ref
                    else:
                        tracking_number_string += ',' + picking_id.carrier_tracking_ref
                        
            url = 'https://arfunding.odoo.com/factor-requests/update'
            obj = { "name":record.name,
                    "customer":self.env.company.name,
                    "customer_taxid":self.env.company.vat,
                    "customer_contact":self.env.user.name,
                    "customer_email":self.env.user.email,
                    "amount_total":record.amount_total,
                    "debtor":record.partner_id.name, 
                    "debtor_email":record.partner_id.email,
                    "debtor_taxid":record.partner_id.vat,
                    "invoice_date":fields.Date.to_string(record.invoice_date),
                    "invoice_date_due":fields.Date.to_string(record.invoice_date_due),
                    "terms":record.invoice_payment_term_id.name,
                    "factoring_proof_tracking_numbers": tracking_number_string,
                    "factoring_proof":str(record.bizylife_backup_info,'utf-8') if record.bizylife_backup_info else None,
                    "purchase_order":str(base64.b64encode(sale_order.bizylife_purchase_order),'utf-8') if sale_order.bizylife_purchase_order else None,
                    "invoice_pdf":str(base64.b64encode(invoice_pdf),'utf-8'),
                    "signature":str(self.env.user.sign_signature,'utf-8'),
                   }

            res = requests.post(url,json=obj)
  
            if(res.status_code == 200):
                json_res = json.loads(res.content)['result']
                print("json_res:",json_res)
                if (json_res['code'] == 200 and json_res['status'] == 'OK'):
                    record.factoring_status = 'sent'
                    msg = "Sent factor request for " + record.name + ".  You will receive correspondence shortly."
                    record.message_post(body=msg)
                elif (json_res['code'] == 200 and json_res['status'] == 'Created Debtor Request'):
                    raise exceptions.ValidationError(str(json_res['code']) + ' ' + json_res['status'] + ': ' + json_res['description'])
                else:
                    raise exceptions.ValidationError(str(json_res['code']) + ' ' + json_res['status'] + ': ' + json_res['description'])
            else:
                raise exceptions.ValidationError("Error with " + record.name + ": \n" + res.reason)

    def cancel(self):
        return False
    
    