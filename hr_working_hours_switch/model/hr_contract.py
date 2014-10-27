#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Extend the hr.contract model.
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


class hr_contract(osv.Model):
    """
    Extend the hr.contract model.
    """

    _inherit = 'hr.contract'
    _columns = {
        'working_hour_switch_id': fields.many2one(
            'hr.working.hours.switch',
            string='Working Hour Switch',
            help='Working Hour Switch'),
        'working_tmpl_id': fields.many2one(
            'hr.working.template',
            string='Working Template',
            help='Working Template'),
    }
