from functools import wraps
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.web.controllers.utils import ensure_db

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    location_company = fields.Char(string='Delivery Location')
    name = fields.Char('Order Reference', required=True, index='trigram', copy=False, default='New')

    @api.onchange('partner_id')
    def _onc_domain_location_company(self):
        self.location_company = self.company_id.street

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            if vals.get('name', 'New') == 'New':
                print('=======create_po')
                current_date = fields.Date.today()

                # Calculate Buddhist Era year
                buddhist_year = current_date.year + 543

                # Get the month name
                month_name = current_date.strftime('%B')

                # Update the sequence name to include year and month
                sequence_name = "YourPrefix/%s-%s BE" % (month_name, buddhist_year)

                # Generate sequence number
                sequence_number = self.env['ir.sequence'].next_by_code(sequence_name) or _('New')

                # Assign the generated sequence number to 'name' field in vals
                vals['name'] = self.env['ir.sequence'].next_by_code(sequence_name) or _('New')
                print('=======name',vals['name'])
            else:
                print('==========else_po')

        # return super(PurchaseOrder, self).create(vals_list)