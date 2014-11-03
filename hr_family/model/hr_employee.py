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
This file add a fields to data family of employee
'''
from openerp import fields, models


class hr_family_type(models.Model):

    '''
    Class to add model to save family type of employee
    '''
    _name = 'hr.family.type'

    name = fields.Char('Name', translate=True, required=True)
    description = fields.Text('Description')


class hr_family(models.Model):

    '''
    Class to register family of employee
    '''
    _name = 'hr.family'

    name = fields.Char('Name', required=True)
    last_name = fields.Char('Last Name')
    date_of_birth = fields.Date('Birth date')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    family_type = fields.Many2one('hr.family.type', 'Kinship')
    upkeep_ok = fields.Boolean(
        'Upkeep', help="Employee is financial aid of this person.")


class hr_employee(models.Model):

    '''
    Inherit hr.employee to added family of employee
    '''
    _inherit = 'hr.employee'

    family_ids = fields.One2many(
        'hr.family', 'employee_id', help='Family of employee')
