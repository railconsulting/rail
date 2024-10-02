import requests,json,base64
from odoo import models,exceptions,fields

class AccountMove(models.Model):
    _inherit = 'account.move'
    bizylife_backup_info = fields.Binary()
    factoring_status = fields.Selection(selection=[('sent','Sent'), # Sent Factoring Request
                                                   ('error','Error'), # Error sending.  Will try again later.
                                                   ('approved','Approved'), # Factoring Request Approved and Pending Debtor Payment.
                                                   ('rejected','Rejected'), # Factoring Request Rejected.
                                                   ('paid','Paid')]) # Invoice fully paid.
    def send_aged_receivable(self):
        aged_receivable = self.env['account.report'].search([('name','=','Aged Receivable')])
        options = aged_receivable.get_options()
        pdf = aged_receivable.export_to_pdf(options)
        url = 'https://arfunding.odoo.com/aged-receivable/update'
        data = {
            "customer": self.env.company.name,
            "customer_taxid" : self.env.company.vat,
            "pdf" : str(base64.b64encode(pdf['file_content']),'utf-8')
        }
  
        res = requests.post(url, json=data)
        print(res)

    def fetch_invoice_debtor_statuses(self):
        url = 'https://arfunding.odoo.com/factor-requests/fetch'
        res = requests.get(url=url,params={"customer_taxid":self.env.company.vat,})
    
        if(res.status_code == 200):
            print('response',res)
            json_res = res.json()
            for factor_request in json_res:
                print(factor_request)
                invoice_id = self.env['account.move'].sudo().search([('name','=',factor_request['factor_request'])])
                if(factor_request['status'] == 'approved'):
                    invoice_id.factoring_status = 'approved'
                elif(factor_request['status'] == 'rejected'):
                    invoice_id.factoring_status = 'rejected'
                elif(factor_request['status'] == 'paid'):
                    invoice_id.factoring_status = 'paid'
                    
                    # code to create journal entry
                    receivable_account_id = None
                    liability_account_id = self.env.company.bizylife_default_factoring_liability_account_id if self.env.company.bizylife_default_factoring_liability_account_id else None 

                    for line in invoice_id.line_ids:
                        if line.debit:
                            print(line.account_id.name)
                            receivable_account_id = line.account_id

                    journal_entry = self.env['account.move'].sudo().create({
                        'move_type': 'entry',
                        'state': 'draft',
                        'partner_id': invoice_id.partner_id.id,
                        # 'journal_id': invoice_id.journal_id.id,
                    })

                    journal_entry.update({
                        # 'name': 'FactorRequest',
                        'line_ids': [
                        (0,0,{
                            'account_id': receivable_account_id.id,
                            'credit': invoice_id.amount_total,
                        }),
                        (0,0,{
                            'account_id': liability_account_id.id,
                            'debit': invoice_id.amount_total,
                            'partner_id': self.env.company.bizylife_factoring_partner_id.id,
                        })],
                        'state': 'posted',
                    })

                    payment_id = None
                    for line in journal_entry.line_ids:
                        print(line,line.credit,line.account_id.name)
                        if line.credit > 0:
                            payment_id = line
                    invoice_id.js_assign_outstanding_line(payment_id.id)
            

        
        url = 'https://arfunding.odoo.com/debtors/fetch'
        res = requests.get(url=url,params={"customer_taxid":self.env.company.vat,})
        if(res.status_code == 200):
            print('response',res)
            json_res = res.json()
            for debtor in json_res:
                debtor_id = self.env['res.partner'].sudo().search([('vat','=',debtor['vat'])])
                print(debtor_id,debtor,debtor['type'])
                if debtor['type'] == 'customer':
                    debtor_id.bizylife_customer_approval_status = debtor['approval_status']
                    self.env.company.update({
                        'bizylife_customer_approval_status': debtor['approval_status']
                    })
                else:
                    debtor_id.bizylife_debtor_approval_status = debtor['approval_status']
                debtor_id.bizylife_rejection_reason = debtor['rejection_reason']

    def factor_invoice(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name','=',record.invoice_origin)])
            if sale_order and hasattr(sale_order,'picking_ids'):
                picking_ids = filter(lambda picking_id : picking_id.location_dest_id.usage == "customer" and picking_id.state == 'done', sale_order.picking_ids)
                have_tracking_numbers = True
                tracking_number_string = None
                for picking_id in picking_ids:
                    if hasattr(picking_id,'carrier_tracking_ref'):
                        if tracking_number_string == None:
                            tracking_number_string = picking_id.carrier_tracking_ref
                        else:
                            tracking_number_string += ',' + picking_id.carrier_tracking_ref
                    else:
                        have_tracking_numbers = False
                    print('tracking numbers',tracking_number_string,picking_ids)
            if (not record.factoring_status == False): 
                raise exceptions.ValidationError(record.name + ' has already been submitted for factoring')
            elif (self.env.company.bizylife_customer_approval_status == 'pending'):
                raise exceptions.ValidationError("Your onboarding questionnaire has been submitted and is pending AR Funding review.  Please wait for us to reach out and then come back here once you are approved.  In the meantime, if you have any questions or need assistance, you can contact us directly at 800-756-3386.")
            elif (not self.env.company.bizylife_customer_approval_status == 'approved'):
                return {
                'name': 'Unlock Instant Working Capital with Odoo Integration',
                'type': 'ir.actions.act_window',
                'res_model': 'bizylife.welcomemessagewizard',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {},
                'target': 'new',
                }
            elif (not record.partner_id.bizylife_debtor_approval_status):
                return {
                'name': 'Debtor not yet approved',
                'type': 'ir.actions.act_window',
                'res_model': 'bizylife.confirmdebtorwizard',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'related_invoice':record.id},
                'target': 'new',
                }
            elif (not record.partner_id.bizylife_debtor_approval_status == 'approved'):
                raise exceptions.ValidationError("Please wait until this debtor is approved for factoring before factoring this invoice, " + record.name + ".")
            elif (record.amount_total >= 5000 and not sale_order.bizylife_purchase_order):
                raise exceptions.ValidationError(record.name + ": Invoices over $5000 require a PO.  Please attach a Purchase Order document on Sales Order " + sale_order.name +" and submit your request again.")
            elif (not record.bizylife_backup_info and not (have_tracking_numbers and tracking_number_string)):
                raise exceptions.ValidationError("Please provide a Bill of Lading or other backup info in the Factoring Backup Info field and submit your request again, " + record.name + ".")
        return {
            'name': 'Factor Invoices Confirmation',
            'type': 'ir.actions.act_window',
            'res_model': 'bizylife.confirmfactorrequests',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'invoice_ids': self.ids,
                'default_message': 'custom message',
            }
        }


        