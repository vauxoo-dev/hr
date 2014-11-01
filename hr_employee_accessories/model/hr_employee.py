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
This file add a field to assign products to employee, this products are
accessories to employee.
'''
from openerp import models, fields


class hr_employee(models.Model):
    '''
    Inherit hr.employee to added m2m to select accessories to employee
    '''
    _inherit = 'hr.employee'

    product_accessory_ids = fields.Many2many(
        'product.product', 'employee_product_accessory_ids', 'product_id',
        'employee_id', 'Product Accessory', help='Indicate the products that \
        provide to the employee, example, shirt XL, etc. Only \
        can see products that have active the field "Accessory Employee"',
        domain=[('hr_employee_accessory_ok', '=', True)],)


class product_template(models.Model):
    '''
    Inherit product.template to add field to indicate if is an accessory to
    employee
    '''
    _inherit = 'product.template'

    hr_employee_accessory_ok = fields.Boolean(
        'Accessory Employee?', help='Indicate if this is an accessory to the \
        employees as shirt, shoes, etc.')
