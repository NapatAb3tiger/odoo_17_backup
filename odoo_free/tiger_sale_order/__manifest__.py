{
    "name": "TIGER SALE ORDER",
    "version": "17.0.0.0.1",
    "category": "SALE",
    'author': 'By Lobanots',
    'website': 'www.lobanots',
    'summary': 'TIGER SALE ORDER',
    'description': """SALE ORDER""",
    "license": "AGPL-3",
    "depends": ['base', 'sale','account'],
    'assets': {
    },
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/account_order_view.xml",
        "views/account_payment_view.xml",
    ],
    'qweb': [],
    "installable": True,
    "application": True,
}
