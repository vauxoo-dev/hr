#!/usr/bin/python
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

import logging

from openerp import netsvc
from openerp.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestLoanCompute(TransactionCase):

    def setUp(self):
        super(TestLoanCompute, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.hr_loan_obj = self.registry('hr.loan')
        self.hr_contract_obj = self.registry('hr.contract')
        self.hr_payslip_obj = self.registry('hr.payslip')
        self.hr_salary_rule_obj = self.registry('hr.salary.rule')
        self.hr_payroll_structure_obj = self.registry('hr.payroll.structure')
        self.account_fiscalyear_obj = self.registry('account.fiscalyear')
        self.account_period_obj = self.registry('account.period')
        self.loan_list_brw = list()
        self.payslip_brw = None
        self.loan_list = list()

    def create_period(self, fiscalyear_data, month):
        cr, uid = self.cr, self.uid

        fy_id = self.account_fiscalyear_obj.search(cr, uid, [
            ('date_start', '=', fiscalyear_data['date_start']),
            ('date_stop', '=', fiscalyear_data['date_stop'])
        ])

        if fy_id:
            fy_brw = self.account_fiscalyear_obj.browse(cr, uid, fy_id[0])

            for period_brw in fy_brw.period_ids:
                for key in month:
                    if period_brw.date_start == month[key][1] and \
                            period_brw.date_stop == month[key][2]:
                        month[key][0] = True

            for key in month:
                if not month[key][0]:
                    month[key][0] = True
        else:
            fiscalyear_id = self.account_fiscalyear_obj.create(
                cr, uid, fiscalyear_data)
            self.account_fiscalyear_obj.create_period(cr, uid, fiscalyear_id)

    def dataloan(self):
        cr, uid = self.cr, self.uid

        struct_id = self.hr_payroll_structure_obj.search(
            cr, uid, [('code', '=', 'Salary loan')])

        contract_id = self.hr_contract_obj.create(cr, uid, {
            'name': 'Ashley Presley Contract',
            'employee_id': 13,  # Ashley Presley
            'type_id': 1,  # Employee
            'wage': 10000,
            'struct_id': struct_id[0],  # Salary with loan
        })

        data_loan = [
            {
                'name': 'Test Loan 1',
                'share_quantity': 8,
                'date_start': '2014-10-29',
                'payment_type': 'bimonthly',
                'amount_approved': '1250',
                'employee_id': contract_id,
                'partner_id': 13,
            },
            {
                'name': 'Test Loan 2',
                'share_quantity': 5,
                'date_start': '2015-01-15',
                'payment_type': 'weekly',
                'amount_approved': '520',
                'employee_id': contract_id,
                'partner_id': 12,
            }
        ]

        for loan_data in data_loan:
            loan_id = self.hr_loan_obj.create(cr, uid, loan_data)
            self.loan_list.append(loan_id)

        payslip_id = self.hr_payslip_obj.create(cr, uid, {
            'name': 'Salary Slip of Ashley Presley for octubre-2014',
            'employee_id': 13,  # Ashley Presley
            'contract_id': contract_id,
            'struct_id': struct_id[0],
            'journal_id': 5,
            'date_from': '2015-02-01',
            'date_to': '2015-02-28',
        })
        self.payslip_brw = self.hr_payslip_obj.browse(cr, uid, payslip_id)

        salary_rule_id = self.hr_salary_rule_obj.search(
            cr, uid, [('name', '=', 'Loan')])
        self.hr_salary_rule_obj.write(cr, uid, salary_rule_id, {
            'account_credit': 9,
        })
        salary_rule_id = self.hr_salary_rule_obj.search(cr, uid,
                                                        [('name', '=',
                                                          'Net Minus Loan')])
        self.hr_salary_rule_obj.write(cr, uid, salary_rule_id, {
            'account_credit': 9,
        })
        salary_rule_id = self.hr_salary_rule_obj.search(cr, uid,
                                                        [('name', '=',
                                                          'Basic')])
        self.hr_salary_rule_obj.write(cr, uid, salary_rule_id, {
            'account_debit': 9,
        })

        fiscalyear_data = {
            'name': '2014',
            'code': '2014',
            'date_start': '2014-01-01',
            'date_stop': '2014-12-31',
        }
        month = {
            10: [False, '2014-10-01', '2014-10-31'],
            11: [False, '2014-11-01', '2014-11-30'],
            12: [False, '2014-12-01', '2014-12-31'],
        }

        self.create_period(fiscalyear_data, month)

        fiscalyear_data = {
            'name': '2015',
            'code': '2015',
            'date_start': '2015-01-01',
            'date_stop': '2015-12-31',
        }
        month = {
            1: [False, '2015-01-01', '2015-01-31'],
            2: [False, '2015-02-01', '2015-02-28'],
            3: [False, '2015-03-01', '2015-03-31'],
            4: [False, '2015-04-01', '2015-04-30'],
            5: [False, '2015-05-01', '2015-05-31'],
        }

        self.create_period(fiscalyear_data, month)

        return True

    def share_test(self, loan_brw, amount):
        error_msg_share_test = 'Error! in share amount'
        for share in loan_brw.share_ids:
            if share.share != amount or share.state != 'unpaid':
                self.assertEquals(error_msg_share_test)

    def date_test(self, loan_brw, ind, date):
        error_msg_date_test = 'Error! in shares payment_date'
        share = loan_brw.share_ids[ind]
        if share.payment_date != date:
            self.assertEquals(error_msg_date_test)

    def date_test_end(self, loan_brw, date):
        error_msg_date_end = 'Error! in loan end date'
        if loan_brw.date_stop != date:
            self.assertEquals(error_msg_date_end)

    def loan_test_bimonthly(self):
        if self.loan_list_brw:
            loan_brw = self.loan_list_brw[0]

            self.share_test(loan_brw, 156.25)
            self.date_test_end(loan_brw, '2016-01-01')
            self.date_test(loan_brw, 0, '2014-10-31')
            self.date_test(loan_brw, 1, '2014-12-31')
            self.date_test(loan_brw, 2, '2015-02-28')
            self.date_test(loan_brw, 3, '2015-04-30')
            self.date_test(loan_brw, 4, '2015-06-30')
            self.date_test(loan_brw, 5, '2015-08-31')
            self.date_test(loan_brw, 6, '2015-10-31')
            self.date_test(loan_brw, 7, '2015-12-31')

        return True

    def loan_test_weekly(self):
        if self.loan_list_brw:
            loan_brw = self.loan_list_brw[1]

            self.share_test(loan_brw, 104)
            self.date_test_end(loan_brw, '2015-02-20')
            self.date_test(loan_brw, 0, '2015-01-22')
            self.date_test(loan_brw, 1, '2015-01-29')
            self.date_test(loan_brw, 2, '2015-02-05')
            self.date_test(loan_brw, 3, '2015-02-12')
            self.date_test(loan_brw, 4, '2015-02-19')

        return True

    def loan_test_fortnightly(self):
        if self.loan_list_brw:
            loan_brw = self.loan_list_brw[0]

            self.share_test(loan_brw, 750)
            self.date_test_end(loan_brw, '2015-06-01')
            self.date_test(loan_brw, 0, '2014-10-31')
            self.date_test(loan_brw, 1, '2014-11-30')
            self.date_test(loan_brw, 2, '2014-12-31')
            self.date_test(loan_brw, 3, '2015-01-31')
            self.date_test(loan_brw, 4, '2015-02-28')
            self.date_test(loan_brw, 5, '2015-03-31')
            self.date_test(loan_brw, 6, '2015-04-30')
            self.date_test(loan_brw, 7, '2015-05-31')

        return True

    def loan_test_monthly(self):
        if self.loan_list_brw:
            loan_brw = self.loan_list_brw[1]

            self.share_test(loan_brw, 600)
            self.date_test_end(loan_brw, '2015-04-01')
            self.date_test(loan_brw, 0, '2015-01-31')
            self.date_test(loan_brw, 1, '2015-02-15')
            self.date_test(loan_brw, 2, '2015-02-28')
            self.date_test(loan_brw, 3, '2015-03-15')
            self.date_test(loan_brw, 4, '2015-03-31')

        return True

    def loan_test_state(self):
        cr, uid = self.cr, self.uid
        error_msg_state = 'Error! in state of loan'
        for loan_brw in self.loan_list_brw:
            if loan_brw.state != 'draft':
                self.assertEquals(error_msg_state)

            # Activate loan
            self.hr_loan_obj.activate_loan(cr, uid, loan_brw.id)

            if loan_brw.state != 'active':
                self.assertEquals(error_msg_state)

    def loan_test_payslip(self):
        cr, uid = self.cr, self.uid
        error_msg_payslip = 'Error! in share of payslip'
        num_loan = []

        self.hr_payslip_obj.compute_sheet(cr, uid, self.payslip_brw.id)
        for payslip in self.payslip_brw.line_ids:
            if payslip.category_id.code == 'LOAN':
                num_loan.append((payslip.id, payslip.total))
            elif payslip.category_id.code == 'NET':
                if payslip.total != 10000:
                    self.assertEquals(error_msg_payslip)
            elif payslip.category_id.code == 'NETLOAN':
                if payslip.total != 8050:
                    self.assertEquals(error_msg_payslip)

        if len(num_loan) != 3:
            self.assertEquals(error_msg_payslip)

        amount_600 = 0
        amount_750 = 0

        for payslip in num_loan:
            if payslip[1] == 600:
                amount_600 += 1
            if payslip[1] == 750:
                amount_750 += 1

        if amount_600 != 2 and amount_750 != 1:
            self.assertEquals(error_msg_payslip)

        if self.payslip_brw.state != 'draft':
            self.assertEquals(error_msg_payslip)

        for share_line in self.payslip_brw.share_line_ids:
            if share_line.state != 'unpaid':
                self.assertEquals(error_msg_payslip)

        self.hr_payslip_obj.signal_workflow(
            cr, uid, [self.payslip_brw.id], 'hr_verify_sheet')
        self.hr_payslip_obj.signal_workflow(
            cr, uid, [self.payslip_brw.id], 'process_sheet')

        if self.payslip_brw.state != 'done':
            self.assertEquals(error_msg_payslip)

    def loan_test_account_move(self):
        error_msg_account = 'Error! in account_move'

        if not self.payslip_brw.move_id:
            self.assertEquals(error_msg_account)

        for aml in self.payslip_brw.move_id.line_id:
            _logger.log(25, "aml.state %s", aml.state)
            if aml.state != 'valid':
                self.assertEquals(error_msg_account)
        num = 0
        if self.payslip_brw.move_id.line_id[num].name == 'Adjustment Entry':
            num += 1
        _logger.log(25, "self.payslip_brw.move_id.line_id[num].credit 8050 %s",
                    self.payslip_brw.move_id.line_id[num].credit)
        if self.payslip_brw.move_id.line_id[num].credit != 8050:
            self.assertEquals(error_msg_account)
        num += 1
        _logger.log(25, "self.payslip_brw.move_id.line_id[num].credit 600 %s",
                    self.payslip_brw.move_id.line_id[num].credit)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]"
                    ".partner_id.id 12 %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.id)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]"
                    ".partner_id.name %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.name)
        if self.payslip_brw.move_id.line_id[num].credit != 600 or \
                self.payslip_brw.move_id.line_id[num].partner_id.id != 12:
            self.assertEquals(error_msg_account)
        num += 1
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]"
                    ".credit 600 %s",
                    self.payslip_brw.move_id.line_id[num].credit)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]."
                    "partner_id.id 12 %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.id)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]."
                    "partner_id.name %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.name)
        if self.payslip_brw.move_id.line_id[num].credit != 600 or \
                self.payslip_brw.move_id.line_id[num].partner_id.id != 12:
            self.assertEquals(error_msg_account)
        num += 1

        _logger.log(25, "self.payslip_brw.move_id.line_id[num]."
                    "credit 750 %s",
                    self.payslip_brw.move_id.line_id[num].credit)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]."
                    "partner_id.id 13 %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.id)
        _logger.log(25, "self.payslip_brw.move_id.line_id[num]."
                    "partner_id.name %s",
                    self.payslip_brw.move_id.line_id[num].partner_id.name)
        if self.payslip_brw.move_id.line_id[num].credit != 750 or \
           self.payslip_brw.move_id.line_id[num].partner_id.id != 13:
            self.assertEquals(error_msg_account)
        num += 1

        _logger.log(25, "self.payslip_brw.move_id.line_id[num]"
                    ".credit 10000 %s",
                    self.payslip_brw.move_id.line_id[num].credit)
        if self.payslip_brw.move_id.line_id[num].debit != 10000:
            self.assertEquals(error_msg_account)

    def test_compute_shares(self):
        cr, uid = self.cr, self.uid

        self.dataloan()

        for loan_id in self.loan_list:

            self.hr_loan_obj.compute_shares(cr, uid, loan_id)
            loan_brw = self.hr_loan_obj.browse(cr, uid, loan_id)

            self.loan_list_brw.append(loan_brw)

            if loan_brw.share_quantity != len(loan_brw.share_ids):
                self.assertEquals('Error! in shares quantity')

        self.loan_test_bimonthly()
        self.loan_test_weekly()

        loan_1 = self.loan_list[0]
        self.hr_loan_obj.write(cr, uid, loan_1, {
            'payment_type': 'monthly',
            'amount_approved': 6000,
        })
        self.hr_loan_obj.compute_shares(cr, uid, loan_1)

        loan_2 = self.loan_list[1]
        self.hr_loan_obj.write(cr, uid, loan_2, {
            'payment_type': 'fortnightly',
            'amount_approved': 3000,
        })
        self.hr_loan_obj.compute_shares(cr, uid, loan_2)

        self.loan_test_fortnightly()
        self.loan_test_monthly()

        self.loan_test_state()
        self.loan_test_payslip()
        self.loan_test_account_move()
