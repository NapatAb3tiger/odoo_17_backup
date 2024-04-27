from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.addons.web.controllers.utils import ensure_db
from bahttext import bahttext
# from num2words import num2words

class ResCompany(models.Model):
    _inherit = 'res.company'

    name_th = fields.Char(string='Name Th')
