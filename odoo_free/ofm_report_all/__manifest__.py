# -*- coding: utf-8 -*-

{
    'name': 'OFM REPORT ALL',
    'author': 'By Lobanots',
    'website': 'www.lobanots',
    'summary': 'OFM REPORT ALL',
    'description': """REPORT""",
    'version': '17.0.0.1',
    'category': 'API',
    'depends': ['base','stock','purchase','product','sale','account','ofm_fields_all'],
    'data': [
        'views/po_report.xml',
        'views/po_report_com.xml',
        'views/po_odc_store_report.xml',
        'views/po_odc_sku_report.xml',

    ],
    'qweb': [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}

