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
                'amount_approved' : 6000,
                'share_quantity' : 8,
                'payment_type' : 'monthly',
                'date_start' : '2014-10-29',
                'employee_id' : contract_id,
                'partner_id' : 13,
                },
                 {
                'name' : 'Test Loan 2',
                'amount_approved' : 3000,
                'share_quantity' : 4,
                'payment_type' : 'fortnightly',
                'date_start' : '2014-10-24',
                'employee_id' : contract_id,
                'partner_id' : 13,
                }
            ]

        self.loan_list = list()

        for loan_data in data_loan:
            loan_id = self.hr_loan_obj.create(cr, uid, loan_data)
            self.loan_list.append(loan_id)

        return True

    def test1(self):
        cr, uid = self.cr, self.uid
        #loan_brw = self.loan_list_brw[0]

        #share_1 = loan_brw.share_ids[0]

        #if share_1.payment_date != '2014-10-31':
        #    self.assertEquals('Error! in shares payment_date')
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

        test1_ok = self.test1()


