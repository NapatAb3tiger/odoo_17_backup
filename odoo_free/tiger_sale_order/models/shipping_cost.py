from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.web.controllers.utils import ensure_db

class ShippingCost(models.Model):
    _name = 'shipping.cost'

    name = fields.Char(string='Name')

