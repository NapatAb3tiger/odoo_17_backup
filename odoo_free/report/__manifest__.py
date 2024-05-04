# -*- coding: utf-8 -*-

{
    "name": "Report",
    "version": "17.0.0.0.1",
    "category": "",
    "author": "Lobanots",
    "website": "www.lobanots",
    'summary': 'Report',
    'description': """Report""",
    "license": "AGPL-3",
    "depends": [ 'base','purchase','sale', 'account'],
    'assets': {

    },
    "data": [

        'report/so_report.xml',
        'report/account_report.xml',
    ],
    'qweb': [],
    "installable": True,
    "application": True,
}
