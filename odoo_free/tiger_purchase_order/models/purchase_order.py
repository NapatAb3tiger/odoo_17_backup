from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.web.controllers.utils import ensure_db

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    contact_phone1 = fields.Char(string='Contact phone')
    shipping_cost = fields.Many2one('shipping.cost', string='Shipping Cost')
    discount_total = fields.Monetary(string='Discount Total', compute='_compute_discount_total')
    contact_id1 = fields.Many2one('res.partner', string='Contact Name', domain=[])

    @api.model_create_multi
    def create(self, vals_list):
        orders = self.browse()
        partner_vals_list = []
        for vals in vals_list:
            company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
            # Ensures default picking type and currency are taken from the right company.
            self_comp = self.with_company(company_id)
            if vals.get('name', 'New') == 'New':
                seq_date = None
                if 'date_order' in vals:
                    seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
                vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
                print('=========name', vals['name'])
                new_name = ""
                time_to = (fields.Datetime.now().year + 543) % 100
                new_name = str(vals['name']).split('X')

                vals['name'] = str(new_name[0]) + str(time_to) + str(new_name[1])
                print('=========name', vals['name'])

            vals, partner_vals = self._write_partner_values(vals)
            partner_vals_list.append(partner_vals)
            orders |= super(PurchaseOrder, self_comp).create(vals)
        for order, partner_vals in zip(orders, partner_vals_list):
            if partner_vals:
                order.sudo().write(partner_vals)  # Because the purchase user doesn't have write on `res.partner`
        return orders

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