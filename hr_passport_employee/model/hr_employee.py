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
This file add a fields to set expedition date and expiration of passport
'''
from openerp import models, fields


class hr_employee(models.Model):
    '''
    Inherit hr.employee to added fields expedition_date & exxpiration_date to
    passport
    '''
    _inherit = 'hr.employee'

    expedition_date_psport = fields.Date(
        'Expedition Date', help='Expedition date of passport of employee')
    expiration_date_psport = fields.Date(
        'Expiration Date', help='Expiration date of passport of employee')
