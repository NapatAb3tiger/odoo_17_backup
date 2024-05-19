# -*- coding: utf-8 -*-

from odoo import fields, api, models, tools,_
from bahttext import bahttext
from num2words import num2words
import locale
from odoo.osv import expression
from odoo.tools import email_re


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_sale_order(self,sale_order_id):
        name_sale_master = self.env['account.move'].search([('order_id.id', '=', sale_order_id)], limit=1)
        sale_master = self.env['sale.order'].search([('name', '=', name_sale_master.sale_line_ids.order_id.name)], limit=1)
        return sale_master

    def get_lines(self, data, max_line):
        # this function will count number of \n
        line_count = data.count("\n")
        if not line_count:
            # print "line 0 - no new line or only one line"
            # lenght the same with line max
            if not len(data) % max_line:
                line_count = len(data) / max_line
            # lenght not the same with line max
            # if less than line max then will be 0 + 1
            # if more than one, example 2 line then will be 1 + 1
            else:
                line_count = len(data) / max_line + 1
        elif line_count:
            # print "line not 0 - has new line"
            # print line_count
            # if have line count mean has \n then will be add 1 due to the last row have not been count \n
            line_count += 1
            data_line_s = data.split('\n')
            for x in range(0, len(data_line_s), 1):
                # print data_line_s[x]
                if len(data_line_s[x]) > max_line:
                    # print "more than one line"
                    line_count += len(data_line_s[x]) / max_line
        if line_count > 1:
            ##############if more then one line, it is new line not new row, so hight will be 80%
            line_count = line_count * 0.8
        return line_count

    def get_break_line(self, max_body_height, new_line_height, row_line_height, max_line_lenght):
        break_page_line = []
        count_height = 0
        count = 1
        for line in self.invoice_line_ids:
            line_name = self.get_lines(line.name, max_line_lenght)
            # remove by row height to line
            # line_height = row_line_height + ((self.get_line(line.name, max_line_lenght)) * new_line_height)
            line_height = row_line_height * line_name
            print('=======line_height',line_height)
            count_height += line_height
            print('=======count_height', count_height)
            if count_height > max_body_height:
                break_page_line.append(count - 1)
                count_height = line_height
            count += 1
        # last page
        break_page_line.append(count - 1)
        print('=======count', count)
        print('=======break_page_line', break_page_line)
        return break_page_line

    def baht_text(self, amount):
        amount = round(amount, 2)
        amount_text = str(amount).split('.')
        text_before_point = amount_text[0]
        text_before_ten_point = text_before_point[len(text_before_point) - 2]
        text_before_last_point = text_before_point[len(text_before_point) - 1]
        if int(text_before_ten_point) == 0 and int(text_before_last_point) == 1:
            text_before_point = bahttext(float(text_before_point)).split('เอ็ดบาท')
            text_before_point = text_before_point[0] + 'บาท'
        else:
            text_before_point = bahttext(float(text_before_point))

        text_after_point = '0.' + amount_text[1]
        after_point = float(text_after_point)
        if float(text_after_point) != 0.0:
            if text_after_point[2] == '0':
                text_after_point = 'หนึ่งสตางค์'
            else:
                text_after_point = bahttext(after_point).split('บาท')
                text_after_point = text_after_point[1]
        else:
            text_after_point = 'ถ้วน'

        baht_text = text_before_point.split('ถ้วน')[0] + text_after_point

        return baht_text