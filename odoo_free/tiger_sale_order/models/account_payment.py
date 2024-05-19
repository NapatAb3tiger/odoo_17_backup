# -*- coding: utf-8 -*-
from collections import defaultdict
from contextlib import ExitStack, contextmanager
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from hashlib import sha256
from json import dumps
import logging
from markupsafe import Markup
import math
import psycopg2
import re
from textwrap import shorten

from odoo import api, fields, models, _, Command
from odoo.addons.account.tools import format_structured_reference_iso
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning
from odoo.tools import frozendict, mute_logger, date_utils

_logger = logging.getLogger(__name__)




class AccountPayment(models.Model):
    _inherit = "account.payment"

    name_account_th = fields.Char(string='Name Account TH', compute='_compute_name_new')
    cheque_type = fields.Char(string='Cheque Type')
    cheque_bank = fields.Char(string='Cheque Bank')
    cheque_branch = fields.Char(string='Cheque Branch')
    cheque_number = fields.Char(string='Cheque Number')
    cheque_date = fields.Date(string='Cheque Date')

    def _compute_name_new(self):
        print('======compu')
        for i in self:
            if i.name:
                new_seq = i.name.split('/')
                time_to = (fields.Datetime.now().year + 543) % 100
                month = "{:02d}".format(fields.Datetime.now().month)
                i.name_account_th = str('SB' + str(time_to) + 'RC' + str(month) + new_seq[2])
                i.cheque_type = i.journal_id.name
                print('========i.name_account_th',i.name_account_th)