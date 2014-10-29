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

from openerp.tests.common import TransactionCase
import csv
import os

class TestLoanCompute(TransactionCase):

    payment_type = {
            'fortnightly': 2,
            'monthly': 1,
            'bimonthly': 0.5,
            'weekly': 7,
            }

    def setUp(self):
        super(TestLoanCompute, self).setUp()
        self.imd_obj = self.registry('ir.model.data')
        self.hr_loan_obj = self.registry('hr.loan')
        self.hr_contract_obj = self.registry('hr.contract')

    def test_create_loan(self):
        cr, uid = self.cr, self.uid

        self.contract = self.hr_loan_obj.create(cr, uid, {
                'name' : 'Ashley Presley Contract',
                'employee_id' : 13,
                'type_id' : 1,
                'wage' : 10000,
                'struct_id' : 4,
            })
        return True

    def test_compute_shares(self):
        cr, uid = self.cr, self.uid


        loan_xml_id_list = ['hr_loan_00' + str(i) for i in xrange(1,5)]
        for loan_xml_id in loan_xml_id_list:
            imd_id = self.imd_obj.search(
                cr, uid,
                [('model', '=', 'hr.loan'), ('name', '=', loan_xml_id)])
            if imd_id:
                imd_brw = self.imd_obj.browse(cr, uid, imd_id)

                self.hr_loan_obj.compute_shares(cr, uid, imd_brw[0].res_id)
                loan_brw = self.hr_loan_obj.browse(cr, uid, imd_brw[0].res_id)
                ####


                current_date = datetime.strptime(hr_loan.date_start, '%Y-%m-%d')
                for ind in xrange(0, loan_brw.share_quantity):

                    if loan_brw.payment_type == 'fortnightly':
                        if current_date.day < 15:
                            current_date = current_date.replace(day=15)
                        elif current_date == self.last_day_of_month(current_date):
                            current_date = current_date + relativedelta(days=15)
                        else:
                            current_date = self.last_day_of_month(current_date)

                    if loan_brw.payment_type == 'weekly':
                        current_date = current_date + relativedelta(days=7)
                    if loan_brw.payment_type == 'monthly':
                        current_date = current_date + relativedelta(days=1)
                        current_date = self.last_day_of_month(current_date)
                    if loan_brw.payment_type == 'bimonthly':
                        if ind == 0:
                            current_date = current_date + relativedelta(days=1)
                            current_date = self.last_day_of_month(current_date)
                        else:
                            current_date = current_date + relativedelta(months=2)
                            current_date = self.last_day_of_month(current_date)



class clase_1(object):

    def __init__(self):
        self.name = ''
        return None
