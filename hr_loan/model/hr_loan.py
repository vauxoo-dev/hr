#!/usr/bin/python
# -*- encoding: utf-8 -*-
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
############# Credits #########################################################
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

from openerp import pooler, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

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
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'state': fields.selection(STATE_LOAN, 'State'),
        'share_ids': fields.one2many('hr.loan.line', 'hr_loan_id', 'Shares'),
        'share_quantity': fields.integer('Share Quantity'),
        'hr_payslip_id': fields.many2one('hr.payslip', 'Payslip ID'),
    }

    _defaults = {
            'state' : 'draft',
            'currency_id': lambda s, c, u, ctx:
                s.pool.get('res.users').browse(c, u, u, context=ctx).company_id.currency_id.id,
            }
    def activate_loan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids,(int,long)) and [ids] or ids
        for brw in self.browse(cr, uid, ids,  context=context):
            self.compute_shares(cr, uid, [brw.id], context=context)
            self.write(cr, uid, [brw.id], {'state':'active'}, context=context)
        return True

    def draft_loan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids,(int,long)) and [ids] or ids
        for brw in self.browse(cr, uid, ids,  context=context):
            self.write(cr, uid, [brw.id], {'state':'draft'}, context=context)
        return True

    def cancel_loan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids,(int,long)) and [ids] or ids
        for brw in self.browse(cr, uid, ids,  context=context):
            self.write(cr, uid, [brw.id], {'state':'cancel'}, context=context)
        return True

    def last_day_of_month(self, date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1) - timedelta(days=1)

    def compute_shares(self, cr, uid, ids, context=None):
        hr_loan_line_obj = self.pool.get('hr.loan.line')
        for hr_loan in self.browse(cr, uid, ids, context=context):
            old_loanline_ids = hr_loan_line_obj.search(cr, uid, [('hr_loan_id', '=', hr_loan.id)], context=context)
            if old_loanline_ids:
                hr_loan_line_obj.unlink(cr, uid, old_loanline_ids, context=context)

            if hr_loan.amount_approved <= 0 or hr_loan.share_quantity <= 0:
                raise osv.except_osv( _("Values not allowed"),
                    _('Amount Approved and Share Quantity must be greater than zero'))

            share = hr_loan.amount_approved / hr_loan.share_quantity

            ds = datetime.strptime(hr_loan.date_start, '%Y-%m-%d')
            for i in xrange(0, hr_loan.share_quantity):

                if hr_loan.payment_type == 'fortnightly':
                    if ds.day < 15:
                        ds = ds.replace(day=15)
                    elif ds.day == 15:
                        ds = self.last_day_of_month(ds)
                    elif ds == self.last_day_of_month(ds):
                        ds = ds + relativedelta(days=15)
                if hr_loan.payment_type == 'weekly':
                    ds = ds + relativedelta(days=7)
                if hr_loan.payment_type == 'monthly':
                    ds = ds + relativedelta(days=1)
                    ds = self.last_day_of_month(ds)
                if hr_loan.payment_type == 'bimonthly':
                    if i == 0:
                        ds = ds + relativedelta(days=1)
                        ds = self.last_day_of_month(ds)
                    else:
                        ds = ds + relativedelta(months=2)
                        ds = self.last_day_of_month(ds)

                hr_loan_line_obj.create(cr, uid, {
                        'name':  "%s %s" % (_('Share'), ds.strftime('%Y-%m-%d')),
                        'payment_date': ds,
                        'state': 'unpaid',
                        'hr_loan_id': hr_loan.id,
                        'share': share,
                    }, context=context)

            self.write(cr, uid, [hr_loan.id], {'date_stop': ds + relativedelta(days=1)}, context=context)
        return True

class hr_loan_line(osv.Model):
    _name = 'hr.loan.line'
    _columns = {
        'name': fields.char('Name'),
        'hr_loan_id': fields.many2one('hr.loan', 'Loan ID'),
        'hr_payslip_id': fields.many2one('hr.payslip', 'Payslip'),
        'payment_date': fields.date('Payment Date'),
        'share': fields.float('Share', help='Share to pay'),
        #~'payslip_line_id': fields.many2one('hr.payslip.line', 'Payslip Line'),
        'partner_id': fields.related('hr_loan_id', 'partner_id',
                                     type='many2one', string='Bank',
                                     relation="res.partner"),
        'employee_id': fields.related('hr_loan_id', 'employee_id',
                                     type='many2one', string='Employee Contract',
                                     relation="hr.contract"),
        #~'paid': fields.boolean('Paid'),
        'state': fields.selection([('unpaid', 'Unpaid'), ('paid', 'Paid')], 'State'),
    }

class hr_payslip(osv.Model):

    _inherit = 'hr.payslip'

    def compute_sheet(self, cr, uid, ids, context=None):
        res = super(hr_payslip, self).compute_sheet(cr, uid, ids, context=context)
        hr_loan_obj = self.pool.get('hr.loan')
        hr_loan_line_obj = self.pool.get('hr.loan.line')

        for payslip in self.browse(cr, uid, ids, context=context):
            hr_loan_line_ids = hr_loan_line_obj.search(cr, uid, [('employee_id', '=',
                payslip.contract_id.id)], context=context)

            payslip_loan_ids = hr_loan_line_obj.search(cr, uid, [('hr_payslip_id', '=', payslip.id)], context=context)
            if payslip_loan_ids:
                #~hr_loan_line_obj.unlink(cr, uid, payslip_loan_ids, context=context)
                hr_loan_line_obj.write(cr, uid, payslip_loan_ids,
                        {'hr_payslip_id':None },context=context)

            total_loan = 0.0

            for loan_line_brw in hr_loan_line_obj.browse(cr, uid,
                    hr_loan_line_ids, context = context):
                if payslip.date_from <= loan_line_brw.payment_date and \
                    loan_line_brw.payment_date <= payslip.date_to and \
                    loan_line_brw.state == 'unpaid' and \
                    loan_line_brw.hr_loan_id.state == 'active':
                    hr_loan_line_obj.write(cr, uid, [loan_line_brw.id],
                            {'hr_payslip_id': payslip.id},context=context)
                    total_loan += loan_line_brw.share
            self.write(cr, uid, [payslip.id], {'total_loan':total_loan},
                    context=context)
        return res

    def _total_loan(self, cr, uid, ids, name, args, context=None):
        res = {}
        for payslip in self.browse(cr, uid, ids, context=context):
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
