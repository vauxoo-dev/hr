#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Definition of the unit tests of the Odoo hr_working_hours module.
"""

###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
###############################################################################
#    Credits:
#    Coded by: Katherine Zaoral <kathy@vauxoo.com>
#    Planified by: Moises Lopez <moylop260@vauxoo.com>
#    Audited by: Moises Lopez <moylop260@vauxoo.com>
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


class test_working_hours(TransactionCase):

    """
    This test object test the correct functionality of the hr working hours
    module.
    This test depends of the data demo of the module, so if the data demo
    changes then the test need to be change too.
    """

    def setUp(self):
        """
        Inicializate method with the resources to be use in the test.
        @return True
        """
        super(test_working_hours, self).setUp()
        # cur, uid = self.cr, self.uid # commented line to avoid unused
        # variable warning until tests are activated.

        # get the model object needed.
        self.wt_obj = self.registry('hr.working.template')
        self.wtl_obj = self.registry('hr.working.template.line')
        self.wte_obj = self.registry('hr.working.template.exception')
        return True

    def test_shift(self):
        """
        This method will make the hr working hours test.
        @return True
        """
        return True
