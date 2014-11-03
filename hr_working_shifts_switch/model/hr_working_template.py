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

from datetime import datetime

from openerp import api
from openerp.osv import fields, osv


class hr_working_template(osv.Model):

    """
    Definition of the model Working Template.
    """

    _name = 'hr.working.template'
    _description = 'Working Template'

    STATE_SELECTION = [
        ('draft', 'Draft'),
        ('done', 'Active'),
        ('cancel', 'Cancelled')
    ]

    _columns = {
        'name': fields.char(
            'Name',
            required=True,
            size=64,
            help='help string'),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True,
                                  help='The status of the working template.',
                                  select=True),
        'contract_ids': fields.one2many(
            'hr.contract',
            'working_tmpl_id',
            string='Contracts',
            readonly=True,
            help='Contracts'),
        'wking_tmpl_line_ids': fields.one2many(
            'hr.working.template.line',
            'working_id',
            string='Working Template Lines',
            help='Working Template Lines'),
        'wking_tmpl_excpt_id': fields.one2many(
            'hr.working.template.exception',
            'working_id',
            string='Working Template Exception',
            help='Working Template Exception'),
        'period': fields.selection(
            [('weekly', 'Weekly'), ('monthly', 'Montly')],
            string='Period',
            help='Period'),
        'current_working_id': fields.many2one(
            'hr.working.template.line',
            string='Current Working Template Line',
            help='Current Working Template Line',
            #~ required=True,
            domain="[('working_id', '=', id)]",
        ),
    }

    def action_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for wk_tmpl in self.browse(cr, uid, ids, context=context):
            self._write(cr, uid, wk_tmpl.id, {'state': 'done'})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for wk_tmpl in self.browse(cr, uid, ids, context=context):
            self._write(cr, uid, wk_tmpl.id, {'state': 'cancel'})
        return True

    def action_draft(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for wk_tmpl in self.browse(cr, uid, ids, context=context):
            self._write(cr, uid, wk_tmpl.id, {'state': 'draft'})
        return True

    def _switch_shift(self, cr, uid, ids=False, context=None):
        if context is None:
            context = {}
        if not ids:
            ids = self.search(cr, uid, [('state', '=', 'done')])
        return self.switch_shift(cr, uid, ids, context=context)

    @api.v7
    def switch_shift(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wk_tmpl_line_obj = self.pool.get('hr.working.template.line')
        wk_tmpl_excep_obj = self.pool.get('hr.working.template.exception')
        wk_tmpl_hsty_obj = self.pool.get('hr.working.template.history')
        contract_obj = self.pool.get('hr.contract')
        for wk_tmpl in self.browse(cr, uid, ids, context=context):
            wk_tmpl_line_ids = wk_tmpl_line_obj.search(cr, uid,
                                                       [('working_id', '=',
                                                       wk_tmpl.id)],)
            wk_tmpl_line_brw = wk_tmpl_line_obj.browse(cr, uid,
                                                       wk_tmpl_line_ids,
                                                       context=context)
            contract_ids = contract_obj.search(cr, uid,
                                               [('working_tmpl_id',
                                               '=', wk_tmpl.id)],)
            if wk_tmpl_line_ids and wk_tmpl.current_working_id:
                if wk_tmpl_line_ids.index(wk_tmpl.current_working_id.id) == \
                        len(wk_tmpl_line_ids) - 1:
                    next_index = 0
                else:
                    next_index = wk_tmpl_line_ids.index(wk_tmpl.
                                                        current_working_id.
                                                        id) + 1
                self._write(cr, uid, [wk_tmpl.id],
                           {'current_working_id':
                            wk_tmpl_line_ids[next_index]})
                if contract_ids:
                    for contract in contract_ids:
                        wk_tmpl_excep_ids = wk_tmpl_excep_obj.search(cr, uid,
                                           [('working_id', '=', wk_tmpl.id),
                                           ('contract_id', '=', contract)],)
                        if wk_tmpl_excep_ids:
                            wk_tmpl_excep_brw = wk_tmpl_excep_obj.browse(cr,
                                            uid, wk_tmpl_excep_ids,
                                            context=context)
                            for exception in wk_tmpl_excep_brw:
                                if datetime.now().strftime('%Y-%m-%d') >=\
                                        exception.date_start and\
                                        datetime.now().strftime('%Y-%m-%d') <=\
                                        exception.date_stop:
                                    contract_obj._write(cr, uid, [contract],
                                               {'working_hours':
                                                exception.
                                                working_scheduler_id.id})
                                    dict_vals = {'working_id': wk_tmpl.id,
                                                 'working_scheduler_id':
                                                 exception.
                                                 working_scheduler_id.id,
                                                 'contract_id': contract,
                                                 'date': datetime.now().
                                                 strftime('%Y-%m-%d')}
                                    wk_tmpl_hsty_obj.\
                                        create_record_history(cr,
                                                    uid, dict_vals,
                                                    context=context)
                                else:
                                    contract_obj._write(cr, uid, [contract],
                                       {'working_hours':
                                        wk_tmpl_line_brw[next_index].
                                        working_scheduler_id.id})
                                    dict_vals = {'working_id': wk_tmpl.id,
                                                 'working_scheduler_id':
                                                 wk_tmpl_line_brw[next_index].
                                                 working_scheduler_id.id,
                                                 'contract_id': contract,
                                                 'date': datetime.now().
                                                 strftime('%Y-%m-%d')}
                                    wk_tmpl_hsty_obj.\
                                        create_record_history(cr,
                                                    uid, dict_vals,
                                                    context=context)
                        else:
                            contract_obj._write(cr, uid, [contract],
                                       {'working_hours':
                                        wk_tmpl_line_brw[next_index].
                                        working_scheduler_id.id})
                            dict_vals = {'working_id': wk_tmpl.id,
                                         'working_scheduler_id':
                                         wk_tmpl_line_brw[next_index].
                                         working_scheduler_id.id,
                                         'contract_id': contract,
                                         'date': datetime.now().
                                         strftime('%Y-%m-%d')}
                            wk_tmpl_hsty_obj.\
                                create_record_history(cr,
                                            uid, dict_vals,
                                            context=context)
        return True


class hr_working_template_line(osv.Model):

    """
    Definition of the model Working Template Line.
    """

    _name = 'hr.working.template.line'
    _description = 'Working Template Line'

    _columns = {
        'sequence': fields.integer('Sequence', help="Sequence"),
        'working_id': fields.many2one(
            'hr.working.template',
            'Working Template',
            help='Working Template'),
        'working_scheduler_id': fields.many2one(
            'resource.calendar',
            'Working Scheduler',
            help='Working Scheduler'),
    }

    _order = 'sequence'
    _rec_name = 'sequence'


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
        'working_scheduler_id': fields.many2one(
            'resource.calendar',
            'Working Scheduler',
            help='Working Scheduler'),
    }


class hr_working_template_history(osv.Model):

    """
    Definition of the model Working Template History.
    """

    _name = 'hr.working.template.history'
    _description = 'Working Template History'
    _columns = {
        'working_id': fields.many2one(
            'hr.working.template',
            string='Working Template',
            help='Working Template'),
        'working_scheduler_id': fields.many2one(
            'resource.calendar',
            'Working Scheduler',
            help='Working Scheduler'),
        'contract_id': fields.many2one(
            'hr.contract',
            string='Contract',
            help='Contract'),
        'date': fields.date('Date'),
        'description': fields.char(
            'Description',
            size=64,
            help='help string'),
        'related_employee_id': fields.related('contract_id',
            'employee_id',
            type='many2one',
            relation='hr.employee',
            string='Employee'),
    }

    def create_record_history(self, cr, uid, dict_vals, context=None):
        if context is None:
            context = {}
        return self._create(cr, uid, dict_vals, context=context)
