{
    'name': 'IBS Accounting Internal Transfer',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Internal Transfer between Bank and Cash Journals',
    'description': """
        Accounting Internal Transfer
        =============================
        This module adds internal transfer functionality between bank and cash journals.
        
        Features:
        ---------
        * Create internal transfers between journals
        * Automatic paired payment creation
        * Journal swapping (source becomes destination and vice versa)
        * Payment type reversal (send becomes receive and vice versa)
        * Validation and constraints
        * Search filters for internal transfers
        
        Based on the functionality from wm_accounting_internal_transfer module.
    """,
    'author': 'IBS',
    'website': '',
    'depends': ['account', 'check_management'],
    'data': [
        'views/account_payment_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

