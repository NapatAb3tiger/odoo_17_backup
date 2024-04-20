from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.web.controllers.utils import ensure_db

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_id1 = fields.Many2one('res.partner', string='Contact Name', domain= [('id','in',[])])
    contact_phone1 = fields.Char(string='Contact phone')
    shipping_cost = fields.Many2one('shipping.cost', string='Shipping Cost')
    discount_total = fields.Monetary(string='Discount Total',compute='_compute_discount_total')
    areebin = fields.Char(string='areebin')

    @api.onchange('partner_id')
    def _onc_domain_contact(self):
        self.areebin = hello

    @api.onchange('partner_id')
    def _onc_domain_contact(self):
        domain = [('parent_id.id','=',self.partner_id.id),('type','=','contact'),('company_type','=','person')]
        return {'domain': {'contact_id1': domain}}

    @api.onchange('contact_id1')
    def _onc_domain_contact_phone(self):
        if self.contact_id1.phone and self.contact_id1.mobile:
            self.contact_phone1 = str(self.contact_id1.phone + ' / ' + self.contact_id1.mobile)
        elif not self.contact_id1.phone and self.contact_id1.mobile:
            self.contact_phone1 = self.contact_id1.mobile
        else:
            self.contact_phone1 = self.contact_id1.phone

    def _compute_discount_total(self):
        for i in self:
            if i.order_line:
                for obj_line in i.order_line:

                    i.discount_total += (obj_line.price_unit * (obj_line.discount / 100) * obj_line.product_uom_qty)
            else:
                i.discount_total = 0