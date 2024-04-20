# -*- coding: utf-8 -*-

{
    'name': 'TIGER REPORT ALL',
    'author': 'By Lobanots',
    'website': 'www.lobanots',
    'summary': 'TIGER REPORT ALL',
    'description': """REPORT""",
    'version': '17.0.0.1',
    'category': 'API',
    'depends': ['base','stock','purchase','sale','account'],
    'data': [
        'views/po_report.xml',
        'views/so_report.xml',
    ],
    'qweb': [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}

