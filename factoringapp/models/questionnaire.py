import requests,json,datetime
from odoo import fields,models,http,api,exceptions
from odoo.tools.safe_eval import safe_eval,wrap_module
# class QuestionnaireWizard(models.Model):
#     _name = "questionnaire.wizard"
#     _description = "Questionnaire Wizard"
#     _inherit = ['mail.thread', 'mail.activity.mixin'] 
    
#     name = fields.Char(required=True,help="Questionnaire Wizard")
#     questions = fields.Many2many('questionnaire.wizard.question')

#     def requestQuestionsFromServer():
#         # add logic to fetch questions from server    
#         print("")


class QuestionnaireWizardQuestion(models.Model):
    _name = "questionnaire.wizard.question"
    _description = "Questionnaire Wizard Question"

    section = fields.Boolean(help="When this is set as true, this acts as a section rather than a question")
    name = fields.Char()
    title = fields.Char(required=True,help="Question")
    question_type = fields.Selection([('dropdown','Dropdown'),('textbox','Text Box'),('numerical','Numerical Value')]) #('multipleChoice','Multiple Choice')
    auto_calculate_formula = fields.Text()
    response_text = fields.Char()
    response_numerical = fields.Float()
    response_dropdown = fields.Many2one('questionnaire.question.option')
    response_options = fields.Many2many('questionnaire.question.option')
    min_validation = fields.Float()
    max_validation = fields.Float()
    dropdown_validation = fields.Many2many('questionnaire.question.option','questionnaire_dropdown_validation', help="Select the valid dropdown answers here")
    
    @api.model
    def compute_defaults(self):
        print("executing this action")
        print(self.env.context)
        records = self.env['questionnaire.wizard.question'].search([('auto_calculate_formula','!=',False)])
        for record in records:
            print("record",record,self)
            print(record.env.context)
            if not (record.response_numerical or record.response_text or record.response_dropdown):            
                eval = safe_eval(record.auto_calculate_formula,{'record':record,'datetime':wrap_module(datetime,['date'])})
                print('evalutation',eval)
                if (record.question_type == 'numerical'):
                    record.response_numerical = eval
                elif (record.question_type == 'textbox'):
                    record.response_text = eval
            
    def send_responses_to_server(self):
        print("sending responses to server")
        responses = self.env['questionnaire.wizard.question'].search([])
        questions = []
        for r in responses:
            response = None
            if r.question_type == 'dropdown':
                response = r.response_dropdown.name
                r.validate_dropdown()
            elif r.question_type == 'numerical':
                response = r.response_numerical
                r.validate_numerical()
            else:
                response = r.response_text
            
            if not response:
                raise exceptions.ValidationError("Please go back and answer " + r.name)
            questions.append({
                'title': r.title,
                'response': response,
            })
        print('self',self,self.env,self.env.uid,self.env.context)
        user_id = self.env['res.users'].search([('id','=',self.env.uid)])
        # company_id = self.env['res.company'].search([('id','=','1')]) 
        company_id = self.env.company
        url = "https://arfunding.odoo.com/customers/update"
        obj = {
            'name' : company_id.name,
            'taxid' : company_id.vat,
            'street': company_id.street,
            'street2': company_id.street2,
            'state_id': company_id.state_id.id,
            'zip': company_id.zip,
            'country_id': company_id.country_id.id,

            'contact_name' : user_id.name,
            'email' : user_id.email,
            'phone' : user_id.phone,

            'questions' : questions,
        }
        res = requests.post(url,json=obj)
        print('response',res)
        company_id.update({
            'bizylife_customer_approval_status' : 'pending'
        })
        return {
        'name': 'Congragulations!',
        'type': 'ir.actions.act_window',
        'res_model': 'bizylife.approvedmessagewizard',
        'view_mode': 'form',
        'view_type': 'form',
        'context': {},
        'target': 'new',
        }
    
    @api.onchange('response_numerical')
    def validate_numerical(self):
        print('running numerical validations')
        if self.question_type == 'numerical' and self.response_numerical:
            
            if self.min_validation and self.response_numerical < self.min_validation:
                print('min validation')
                raise exceptions.ValidationError("You answered that you invoice $" + str(self.response_numerical) + " monthly but AR Funding requires a minimum of $"
                                                + str(self.min_validation) + " monthly.  Unfortunately, you are not the right candidate to work with AR Funding at this time.")
            if self.max_validation and self.response_numerical > self.max_validation:
                raise exceptions.ValidationError("You answered that you invoice $" + str(self.response_numerical) + " monthly but AR Funding requires a maximum of $"
                                                + str(self.max_validation) + " monthly.  Unfortunately, you are not the right candidate to work with AR Funding at this time.")
    
    @api.onchange('response_dropdown')
    def validate_dropdown(self):      
        print('running dropdown validations',self.question_type,self.response_dropdown,self.response_options)
        valid_options = []

        for option in self.dropdown_validation:
            valid_options.append(option.name)

        if self.question_type == 'dropdown' and self.response_dropdown:
            if not self.response_dropdown.name in valid_options:
                raise exceptions.ValidationError("AR Funding does not currently work in this selected industry.  Unfortunately, " +
                                                 "you are not the right candidate to work with AR Funding at this time.")

    def _default_response_numerical(self):
        if self.question_type == 'numerical' and self.auto_calculate_formula and not self.response_text:
            print('numerical calculation')
    
    def fetch_default_questions(self):
        print("fetching default questions")

    def submit_answers(self):
        print("answers submitted")

class QuestionnaireWizardQuestionOptions(models.Model):
    _name = "questionnaire.question.option"
    _description = ""

    name = fields.Char()
    reference = fields.One2many(comodel_name='questionnaire.wizard.question',inverse_name='response_options')

    




