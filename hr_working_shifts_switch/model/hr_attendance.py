#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Inherit the hr.attendance model.
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

from openerp.osv import fields, osv


class hr_attendance(osv.Model):

    """
    Inherit the hr.attendance model.
    """

    _inherit = 'hr.attendance'
    _columns = {
        'working_id': fields.many2one(
            'hr.working.template',
            'Working Template',
            help='Working Template'),
        'contract_id': fields.many2one(
            'hr.contract',
            'Contract',
            help='Contract'),
    }
