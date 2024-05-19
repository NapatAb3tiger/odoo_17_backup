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



class AccountMove(models.Model):
    _inherit = "account.move"
    name_account_th = fields.Char(string='Name Account TH')
    billing_note_name = fields.Char(string='Name Billing Note TH')
    create_billing_note_date = fields.Date(string='Cheque Date')

    def button_create_billing_note(self):
        self.billing_note_name = self.env['ir.sequence'].next_by_code('account.move')
        print('===========self.billing_note_name', self.billing_note_name)
        new_name = ""
        time_to = (fields.Datetime.now().year + 543) % 100
        new_name = str(self.billing_note_name).split('X')

        self.billing_note_name = str(new_name[0]) + str(time_to) + str(new_name[1])
        self.create_billing_note_date = fields.Datetime.now()

        print('===========self.billing_note_name', self.billing_note_name)


    @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'payment_id')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m._origin.id))

        for move in self:
            if move.state == 'cancel':
                continue
            move_has_name = move.name and move.name != '/'
            if move_has_name or move.state != 'posted':
                print('====move.name', move.name)
                if not move.posted_before and not move._sequence_matches_date():
                    print('====move.name1', move.name)
                    if move._get_last_sequence():
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    print('====move.name2', move.name)
                    if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence():
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()):
                print('====move.name3', move.name)
                move._set_next_sequence()
                print('====self.name', self.name)

        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
        print('====self.name1', self.name)
        self._inverse_name()
        if self.name and self.name != 'Draft' and self.name != '/':
            new_name = self.name.split('/')
            print('==new_name', new_name)
            name_01 = new_name[0].split('B')
            print('==name_01', name_01)
            time_to = (fields.Datetime.now().year + 543) % 100
            print('==time_to', time_to)
            month = "{:02d}".format(fields.Datetime.now().month)
            print('==month', month)
            total_name = str(name_01[0] + 'B' + str(time_to) + name_01[1] + month + new_name[2])
            print('====total_name', total_name)
            self.name_account_th = total_name
            print('====total_name1', self.name)

    def _set_next_sequence(self):
        """Set the next sequence.

        This method ensures that the field is set both in the ORM and in the database.
        This is necessary because we use a database query to get the previous sequence,
        and we need that query to always be executed on the latest data.

        :param field_name: the field that contains the sequence.
        """
        self.ensure_one()
        last_sequence = self._get_last_sequence()
        new = not last_sequence
        if new:
            last_sequence = self._get_last_sequence(relaxed=True) or self._get_starting_sequence()

        format_string, format_values = self._get_sequence_format_param(last_sequence)
        sequence_number_reset = self._deduce_sequence_number_reset(last_sequence)
        if new:
            date_start, date_end = self._get_sequence_date_range(sequence_number_reset)
            prefix_new = format_values['prefix1'].split('/')
            total_name = str('SB') + prefix_new[0] + '/'
            format_values['prefix1'] = str(total_name)
            format_values['seq'] = 0
            format_values['year'] = self._truncate_year_to_length(date_start.year, format_values['year_length'])
            format_values['year_end'] = self._truncate_year_to_length(date_end.year, format_values['year_end_length'])
            format_values['month'] = date_start.month

        # before flushing inside the savepoint (which may be rolled back!), make sure everything
        # is already flushed, otherwise we could lose non-sequence fields values, as the ORM believes
        # them to be flushed.
        self.flush_recordset()
        # because we are flushing, and because the business code might be flushing elsewhere (i.e. to
        # validate constraints), the fields depending on the sequence field might be protected by the
        # ORM. This is not desired, so we already reset them here.
        registry = self.env.registry
        triggers = registry._field_triggers[self._fields[self._sequence_field]]
        for inverse_field, triggered_fields in triggers.items():
            for triggered_field in triggered_fields:
                if not triggered_field.store or not triggered_field.compute:
                    continue
                for field in registry.field_inverses[inverse_field[0]] if inverse_field else [None]:
                    self.env.add_to_compute(triggered_field, self[field.name] if field else self)
        while True:
            print('======format_values', format_values)
            format_values['seq'] = format_values['seq'] + 1
            sequence = format_string.format(**format_values)
            try:
                with self.env.cr.savepoint(flush=False), mute_logger('odoo.sql_db'):
                    self[self._sequence_field] = sequence
                    self.flush_recordset([self._sequence_field])
                    break
            except DatabaseError as e:
                # 23P01 ExclusionViolation
                # 23505 UniqueViolation
                if e.pgcode not in ('23P01', '23505'):
                    raise e
        self._compute_split_sequence()
        self.flush_recordset(['sequence_prefix', 'sequence_number'])

