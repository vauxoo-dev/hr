# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#
#    Coded by: Luis Torres (luis_t@vauxoo.com)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
'''
This file add a field to assign blood type to employee.
'''
from openerp import models, fields, api


class hr_employee(models.Model):
    '''
    Inherit hr.employee to added field blood type
    '''
    _inherit = 'hr.employee'

    @api.model
    def _get_blood_types(self):
        types = [
            ('a_pos', 'A+'),
            ('a_neg', 'A-'),
            ('b_pos', 'B+'),
            ('b_neg', 'B-'),
            ('o_pos', 'O+'),
            ('o_neg', 'O-'),
            ('ab_pos', 'AB+'),
            ('ab_neg', 'AB-'),
            ]
        return types

    blood_type = fields.Selection(
        _get_blood_types, 'Blood Type', type="char",
        help='Blood type employee')
