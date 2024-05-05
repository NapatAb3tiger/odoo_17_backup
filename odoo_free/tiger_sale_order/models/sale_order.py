from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.addons.web.controllers.utils import ensure_db
from bahttext import bahttext


# from num2words import num2words

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_phone1 = fields.Char(string='Contact phone')
    shipping_cost = fields.Many2one('shipping.cost', string='Shipping Cost')
    discount_total = fields.Monetary(string='Discount Total', compute='_compute_discount_total')
    contact_id1 = fields.Many2one('res.partner', string='Contact Name', domain=[])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order'])
                ) if 'date_order' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _("New")

            print('=========name', vals['name'])
            new_name = ""
            time_to = (fields.Datetime.now().year + 543) % 100
            new_name = str(vals['name']).split('X')

            vals['name'] = str(new_name[0]) + str(time_to) + str(new_name[1])
            print('=========name', vals['name'])
        return super().create(vals_list)

    @api.onchange('partner_id')
    def _on_partner_change_filter_contacts(self):
        domain = [
            ('parent_id.id', '=', self.partner_id.id),
            ('type', '=', 'contact'),
            ('company_type', '=', 'person')
        ]
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

