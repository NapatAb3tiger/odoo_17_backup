from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.web.controllers.utils import ensure_db

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    location_company = fields.Char(string='Delivery Location')

    @api.onchange('partner_id')
    def _onc_domain_location_company(self):
        self.location_company = self.company_id.street
