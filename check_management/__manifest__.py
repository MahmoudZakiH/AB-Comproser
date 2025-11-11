# -*- coding: utf-8 -*-
{
    'name': "IBS Check Management",

    'summary': """
        This module is used to manage checks in Odoo.
    """,

    'author': "IBS",
    'website': "https://www.ibs-egy.com",

    'category': 'Accounting',
    'version': '18.0',

    'depends': ['base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/payment_check.xml',
        'views/journal.xml',
        'views/transient.xml',
        'views/partial_transient.xml',
        'views/payment_check_line.xml',
        'views/payment_check_line_line.xml',
        'views/move_menus.xml',
        'views/check_history.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}