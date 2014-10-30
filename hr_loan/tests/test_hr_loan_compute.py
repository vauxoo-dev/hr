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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tests.common import TransactionCase
import csv
import os

class TestLoanCompute(TransactionCase):

    def setUp(self):
        super(TestLoanCompute, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.hr_loan_obj = self.registry('hr.loan')
        self.hr_contract_obj = self.registry('hr.contract')
        self.loan_list_brw = list()

    def dataloan(self):
        cr, uid = self.cr, self.uid

        contract_id = self.hr_contract_obj.create(cr, uid, {
                'name' : 'Ashley Presley Contract',
                'employee_id' : 13, #Ashley Presley
                'type_id' : 1, #Employee
                'wage' : 10000,
                'struct_id' : 4, #Salary with loan
            })

        data_loan = [
                {
                'name' : 'Test Loan 1',
                'share_quantity' : 8,
                'date_start' : '2014-10-29',
                'payment_type' : 'bimonthly',
                'amount_approved' : '1250',
                'employee_id' : contract_id,
                'partner_id' : 13,
                },
                 {
                'name' : 'Test Loan 2',
                'share_quantity' : 5,
                'date_start' : '2015-01-15',
                'payment_type' : 'weekly',
                'amount_approved' : '520',
                'employee_id' : contract_id,
                'partner_id' : 13,
                }
            ]

        self.loan_list = list()

        for loan_data in data_loan:
            loan_id = self.hr_loan_obj.create(cr, uid, loan_data)
            self.loan_list.append(loan_id)

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

    def test_compute_shares(self):
        cr, uid = self.cr, self.uid

        data_ok = self.dataloan()

        for loan_id in self.loan_list:

            self.hr_loan_obj.compute_shares(cr, uid, loan_id)
            loan_brw = self.hr_loan_obj.browse(cr, uid, loan_id)

            self.loan_list_brw.append(loan_brw)

            current_date = datetime.strptime(loan_brw.date_start, '%Y-%m-%d')

            if loan_brw.share_quantity != len(loan_brw.share_ids):
                self.assertEquals('Error! in shares quantity')

        self.loan_test_bimonthly()
        self.loan_test_weekly()

        loan_1 = self.loan_list[0]
        self.hr_loan_obj.write(cr, uid, loan_1, {
                'payment_type' : 'monthly',
                'amount_approved' : 6000,
                                    })
        self.hr_loan_obj.compute_shares(cr, uid, loan_1)

        loan_2 = self.loan_list[1]
        self.hr_loan_obj.write(cr, uid, loan_2, {
                'payment_type' : 'fortnightly',
                'amount_approved' : 3000,
                                    })
        self.hr_loan_obj.compute_shares(cr, uid, loan_2)

        self.loan_test_monthly()
        self.loan_test_fortnightly()


        #loan_brw = self.hr_loan_obj.browse(cr, uid, self.loan_list[0])
        #self.loan_list_brw[0] = loan_brw

