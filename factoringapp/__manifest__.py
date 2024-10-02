{
    'name': "Factoring App",
    'version': '1.0',
    'depends': ['base','account','sale','sign'],
    'author': "Associated Receivables Funding",
    'license': 'OPL-1',
    'category': 'Accounting/Accounting',
    'description': """
    Transform your cash flow management by converting unpaid invoices into immediate working capital, all within the Odoo platform.

    The AR Funding integration for Odoo brings the power of instant invoice financing directly to your Odoo ERP system. Designed to streamline your financial operations, our solution allows businesses to convert their outstanding invoices into immediate cash, providing much-needed liquidity and eliminating the wait for customer payments.
    With AR Funding, Odoo users can effortlessly access funds tied up in unpaid invoices, ensuring smooth operations and financial stability. Whether you're a small business or a large enterprise, our integration offers a user-friendly, flexible, and efficient way to improve cash flow management and sustain growth.
    <keywords>
    Factoring
    Cash Flow
    Financing
    AR Funding
    Associated Receivables
    Invoice
    Invoice Factoring
    Working Capital
    """,
    'installable': True,
    'application': True,
    'website': "https://www.arfunding.com",
    'images': ["images/arfunding.gif"],
    'data': [
        'views/factor_button.xml',
        'views/invoice.xml',
        'views/sale_order.xml',
        'views/confirm_debtor_wizard.xml',
        'views/confirm_factor_requests_wizard.xml',
        'views/welcome_message_wizard.xml',
        'views/approved_message_wizard.xml',
        'views/questionnaire.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml',
        'security/security.xml',
        'data/scheduled_actions.xml',
        'data/server_actions.xml',
        'data/default_questions.xml',
        'data/initial_function_calls.xml',
        'security/ir.model.access.csv',
    ],
}