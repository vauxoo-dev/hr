#!/usr/bin/python
# -*- encoding: utf-8 -*-
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

{
    'name': 'Working Hours Shifts',
    'version': '1.0',
    'author': 'Vauxoo',
    'website': 'http://www.vauxoo.com/',
    'category': '',
    'description': '''
Working Hours Shifts
====================

There is a need to change and employee or contract turn periodically in an
automatic way. How ever the schedule working hours can be manually change
for a particulary turn, that's the working hour exceptions.

This module add new models:

- Working Template (hr.working.template)
- Working Template Line (hr.working.template.line)
- Working Template Exception (hr.working.template.exception)
''',
    'depends': [
        'hr',
        'hr_contract',
        'hr_attendance',
        'resource',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/hr_working_hours_view.xml',
        'view/hr_contract_view.xml',
        'view/hr_attendance_view.xml',
        'data/data_ir_cron.xml',
    ],
    'demo': [
        'demo/hr_working_template_demo.xml',
    ],
    'test': [],
    'qweb': [],
    'js': [],
    'css': [],
    'active': False,
    'installable': True,
}
