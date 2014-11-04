# -*- encoding: utf-8 -*-
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
# ############ Credits ########################################################
#    Coded by: Yanina Aular <yani@vauxoo.com>
#    Planified by: Moises Lopez <moises@vauxoo.com>
#    Audited by: Humberto Arocha <hbto@vauxoo.com>
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from copy import deepcopy
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp.tools.translate import _

PAYMENT_TYPE = [
    ('fortnightly', 'Fortnightly'),
    ('monthly', 'Monthly'),
    ('bimonthly', 'Bi-Monthly'),
    ('weekly', 'Weekly'),
]

STATE_LOAN = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('cancel', 'Cancel'),
    ('done', 'Done'),
]


class hr_loan(osv.Model):
    _name = 'hr.loan'
    _columns = {
        'name': fields.char('Name', translate=True),
        'amount_approved': fields.float('Amount approved', help='Amount approved \
            for loan'),
        'payment_type': fields.selection(PAYMENT_TYPE, 'Payment Type'),
        'partner_id': fields.many2one('res.partner', 'Bank'),
        'employee_id': fields.many2one('hr.contract', 'Employee Contract'),
        'date_start': fields.date('Start Date'),
        'date_stop': fields.date('End Date'),
        'company_id': fields.many2one('res.company', 'Company'),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'state': fields.selection(STATE_LOAN, 'State'),
        'share_ids': fields.one2many('hr.loan.line', 'hr_loan_id', 'Shares'),
        'share_quantity': fields.integer('Share Quantity'),
        'hr_payslip_id': fields.many2one('hr.payslip', 'Payslip ID'),
    }

    _defaults = {
        'state': 'draft',
        'currency_id': lambda self, cur, uid, ctx:
        self.pool.get('res.users').browse(
            cur, uid, uid, context=ctx).company_id.currency_id.id,
        'company_id': lambda self, cur, uid, ctx:
        self.pool.get('res.users').browse(
            cur, uid, uid, context=ctx).company_id.id,
    }

    def activate_loan(self, cur, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        for brw in self.browse(cur, uid, ids, context=context):
            self.compute_shares(cur, uid, [brw.id], context=context)
            self._write(
                cur, uid, [brw.id], {'state': 'active'}, context=context)
        return True

    def draft_loan(self, cur, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        for brw in self.browse(cur, uid, ids, context=context):
            for loan_share in brw.share_ids:
                if loan_share.state == 'paid':
                    raise osv.except_osv(_("Set to Draft is not allowed"),
                                         _('There are paid lines.'))
            self._write(cur, uid, [brw.id],
                        {'state': 'draft'}, context=context)
        return True

    def cancel_loan(self, cur, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        for brw in self.browse(cur, uid, ids, context=context):
            self._write(cur, uid, [brw.id],
                        {'state': 'cancel'}, context=context)
        return True

    def last_day_of_month(self, date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - timedelta(days=1)

    def compute_shares(self, cur, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        hr_loan_line_obj = self.pool.get('hr.loan.line')
        for hr_loan_brw in self.browse(cur, uid, ids, context=context):
            old_loanline_ids = hr_loan_line_obj.search(
                cur, uid, [('hr_loan_id', '=', hr_loan_brw.id)],
                context=context)
            if old_loanline_ids:
                hr_loan_line_obj.unlink(
                    cur, uid, old_loanline_ids, context=context)

            if hr_loan_brw.amount_approved <= 0 or\
               hr_loan_brw.share_quantity <= 0:
                raise osv.except_osv(
                    _("Values not allowed"),
                    _('Amount Approved and Share Quantity\
                        must be greater than zero'))

            share = hr_loan_brw.amount_approved / hr_loan_brw.share_quantity

            current_date = datetime.strptime(hr_loan_brw.date_start,
                                             '%Y-%m-%d')
            for ind in xrange(0, hr_loan_brw.share_quantity):

                if hr_loan_brw.payment_type == 'fortnightly':
                    if current_date.day < 15:
                        current_date = current_date.replace(day=15)
                    elif current_date == self.last_day_of_month(current_date):
                        current_date = current_date + relativedelta(days=15)
                    else:
                        current_date = self.last_day_of_month(current_date)

                if hr_loan_brw.payment_type == 'weekly':
                    current_date = current_date + relativedelta(days=7)
                if hr_loan_brw.payment_type == 'monthly':
                    current_date = current_date + relativedelta(days=1)
                    current_date = self.last_day_of_month(current_date)
                if hr_loan_brw.payment_type == 'bimonthly':
                    if ind == 0:
                        current_date = current_date + relativedelta(days=1)
                        current_date = self.last_day_of_month(current_date)
                    else:
                        current_date = current_date + relativedelta(months=2)
                        current_date = self.last_day_of_month(current_date)

                hr_loan_line_obj.create(cur, uid, {
                    'name': "%s %s %s (%s)" % (
                        hr_loan_brw.name,
                        _('Share'),
                        ind + 1,
                        current_date.strftime('%Y-%m-%d')),
                    'payment_date': current_date,
                    'state': 'unpaid',
                    'hr_loan_id': hr_loan_brw.id,
                    'share': share,
                }, context=context)

            self._write(cur, uid, [hr_loan_brw.id], {
                'date_stop': current_date + relativedelta(days=1)},
                context=context)
        return True


class hr_loan_line(osv.Model):
    _name = 'hr.loan.line'
    _columns = {
        'name': fields.char('Name'),
        'hr_loan_id': fields.many2one('hr.loan', 'Loan ID'),
        'hr_payslip_id': fields.many2one('hr.payslip', 'Payslip'),
        'payment_date': fields.date('Payment Date'),
        'share': fields.float('Share', help='Share to pay'),
        'partner_id': fields.related('hr_loan_id', 'partner_id',
                                     type='many2one', string='Bank',
                                     relation="res.partner"),
        'employee_id': fields.related(
            'hr_loan_id', 'employee_id',
            type='many2one',
            string='Employee Contract',
            relation="hr.contract"),
        'company_id': fields.related('hr_loan_id', 'company_id',
                                     type='many2one', string='Company',
                                     relation="res.company"),
        'currency_id': fields.related('hr_loan_id', 'currency_id',
                                      type='many2one', string='Currency',
                                      relation="hr.contract"),
        'state': fields.selection(
            [('unpaid', 'Unpaid'), ('paid', 'Paid')], 'State'),
    }


class hr_payslip(osv.Model):
    _inherit = 'hr.payslip'

    def get_payslip_lines(self, cur, uid, contract_ids, payslip_id, context):
        if context is None:
            context = {}
        contract_ids = isinstance(
            contract_ids, (int, long)) and [contract_ids] or contract_ids
        result = super(hr_payslip, self).get_payslip_lines(
            cur, uid, contract_ids, payslip_id, context=context)

        payslip_obj = self.pool.get('hr.payslip')
        payslip = payslip_obj.browse(cur, uid, payslip_id, context=context)

        loan_brw = False

        for ind in result:
            if ind['code'] == 'LOAN':
                loan_brw = ind
                result.remove(ind)

        if loan_brw:
            if payslip.share_line_ids:
                for share_brw in payslip.share_line_ids:
                    amount = share_brw.share
                    line = deepcopy(loan_brw)
                    line['name'] = share_brw.name
                    line['amount'] = amount
                    line['loan_line_id'] = share_brw.id
                    result.append(line)

        return result

    def compute_sheet(self, cur, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        hr_loan_line_obj = self.pool.get('hr.loan.line')

        for payslip in self.browse(cur, uid, ids, context=context):
            hr_loan_line_ids = hr_loan_line_obj.search(
                cur, uid, [('employee_id', '=',
                           payslip.contract_id.id)], context=context)

            payslip_loan_ids = hr_loan_line_obj.search(
                cur, uid,
                [('hr_payslip_id', '=', payslip.id)], context=context)
            if payslip_loan_ids:
                hr_loan_line_obj.write(
                    cur, uid,
                    payslip_loan_ids, {'hr_payslip_id': None}, context=context)

            total_loan = 0.0

            for loan_line_brw in hr_loan_line_obj.browse(
                    cur, uid, hr_loan_line_ids, context=context):
                if payslip.date_from <= loan_line_brw.payment_date and \
                        loan_line_brw.payment_date <= payslip.date_to and \
                        loan_line_brw.state == 'unpaid' and \
                        loan_line_brw.hr_loan_id.state == 'active':
                    hr_loan_line_obj.write(
                        cur, uid, [loan_line_brw.id],
                        {'hr_payslip_id': payslip.id}, context=context)
                    total_loan += loan_line_brw.share
            self._write(cur, uid, [payslip.id], {'total_loan': total_loan},
                        context=context)
        res = super(hr_payslip, self).compute_sheet(
            cur, uid, ids, context=context)
        return res

    def process_sheet(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        result = super(hr_payslip, self).process_sheet(
            cr, uid, ids, context=context)

        hr_loan_line_pool = self.pool.get('hr.loan.line')
        for ind in self.browse(cr, uid, ids, context=context):
            if ind.share_line_ids:
                for slip in ind.share_line_ids:
                    hr_loan_line_pool.write(cr, uid, [slip.id],
                                            {'state': 'paid'}, context=context)
        return result

    def _total_loan(self, cur, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        res = {}
        for payslip in self.browse(cur, uid, ids, context=context):
            res[payslip.id] = {
                'total_loan': 0.0
            }
            for line in payslip.share_line_ids:
                res[payslip.id]['total_loan'] += line.share
        return res

    _columns = {
        'share_line_ids': fields.one2many('hr.loan.line', 'hr_payslip_id',
                                          'Share Line'),
        'total_loan': fields.float('Total Loan', help='Total Loan'),
    }


class hr_payslip_line(osv.Model):

    _inherit = 'hr.payslip.line'

    _columns = {
        'loan_line_id': fields.many2one('hr.loan.line', 'Loan Line'),
    }
