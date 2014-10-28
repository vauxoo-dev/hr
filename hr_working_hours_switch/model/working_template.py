#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Create new openerp models working.template, working.template.line and
working.template.exception.
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


class hr_working_template(osv.Model):
    """
    Definition of the model Working Template.
    """

    _name = 'hr.working.template'
    _description = 'Working Template'
    _columns = {
        'name': fields.char(
            'Name',
            required=True,
            size=64,
            help='help string'),
        'contract_ids': fields.one2many(
            'hr.contract',
            'working_hour_switch_id',
            string='Contracts',
            help='Contracts'),
        'wking_tmpl_line_ids': fields.one2many(
            'hr.working.template.line',
            'working_id',
            string='Working Template Lines',
            help="Working Template Lines"),
        'wking_tmpl_excpt_id': fields.many2one(
            'hr.working.template.exception',
            string='Working Template Exception',
            help="Working Template Exception"),
        'period': fields.selection(
            [('weekly', 'Weekly'), ('monthly', 'Montly')],
            string='Period',
            help='Period'),
        'current_working_id': fields.many2one(
            'hr.working.template.line',
            string='Current Working Template',
            help='Current Working Template'),
    }


class hr_working_template_line(osv.Model):
    """
    Definition of the model Working Template Line.
    """

    _name = 'hr.working.template.line'
    _description = 'Working Template Line'
    _order = 'seq'
    _rec_name = 'working_id'
    _columns = {
        'seq': fields.integer('Sequence', help="Sequence"),
        'working_id': fields.many2one(
            'hr.working.template',
            'Working Template',
            help='Working Template'),
    }


class hr_working_template_exception(osv.Model):
    """
    Definition of the model Working Template Exception.
    """

    _name = 'hr.working.template.exception'
    _description = 'Working Template Exception'
    _columns = {
        'date_start': fields.date('Start Date'),
        'date_stop': fields.date('Stop Date'),
        'working_id': fields.many2one(
            'hr.working.template',
            string='Working Template',
            help='Working Template'),
        'contract_id': fields.many2one(
            'hr.contract',
            string='Contract',
            help='Contract'),
    }
