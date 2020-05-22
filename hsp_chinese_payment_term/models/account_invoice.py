# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import math
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"

    option = fields.Selection(selection_add=[('chinese_month_pay','月结')])#加选择项
    start_day = fields.Integer(string='计费开始日',default=1,help='如果填1就是1号开始到月底，如果填26，就是: 上月26号 <= 订单 <= 当月25号')


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    
    def compute(self, value, date_ref=False, currency=None):
        self.ensure_one()
        date_ref = date_ref or fields.Date.today()
        amount = value
        sign = value < 0 and -1 or 1
        result = []
        if not currency and self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        elif not currency:
            currency = self.env.company.currency_id
        for line in self.line_ids:
            if line.value == 'fixed':
                amt = sign * currency.round(line.value_amount)
            elif line.value == 'percent':
                amt = currency.round(value * (line.value_amount / 100.0))
            elif line.value == 'balance':
                amt = currency.round(amount)
            next_date = fields.Date.from_string(date_ref)
            if line.option == 'day_after_invoice_date':
                next_date += relativedelta(days=line.days)
                if line.day_of_the_month > 0:
                    months_delta = (line.day_of_the_month < next_date.day) and 1 or 0
                    next_date += relativedelta(day=line.day_of_the_month, months=months_delta)
            elif line.option == 'day_following_month':
                next_date += relativedelta(day=line.days, months=1)
            elif line.option == 'day_current_month':
                next_date += relativedelta(day=line.days, months=0)
            elif line.option == 'chinese_month_pay':
                    tem = line.days%30
                    if tem == 0:
                        tem = 30
                    tem_month = math.ceil(line.days/30.0)
                    tem_day = int(date_ref.strftime('%d'))
                    if line.start_day == 1 :
                        pass
                    elif tem_day >= line.start_day:
                        tem_month = tem_month + 1
                    next_date += relativedelta(day=tem, months=tem_month)
            result.append((fields.Date.to_string(next_date), amt))
            amount -= amt
        amount = sum(amt for _, amt in result)
        dist = currency.round(value - amount)
        if dist:
            last_date = result and result[-1][0] or fields.Date.today()
            result.append((last_date, dist))
        return result