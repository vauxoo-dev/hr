# -*- encoding: utf-8 -*-
# ##############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
# ############ Credits ########################################################
#    Coded by: Yanina Aular <yani@vauxoo.com>
#    Planified by: Moises Lopez <moises@vauxoo.com>
#    Audited by: Humberto Arocha <hbto@vauxoo.com>
# ##############################################################################
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
# ##############################################################################
from openerp.osv import fields, osv, _


class hr_salary_rule(osv.osv):

    _inherit = 'hr.salary.rule'

    def _get_selection_partner_aml(self, cr, uid, context=None):
        # res = super(hr_salary_rule,
        #    self)._get_selection_partner(cr, uid, context=context)
        # TODO actived when exist function in origin module
        res = []
        # TODO deprecated append by origin module
        res.append(('default', _('By default')))
        res.append(('loan', _('Use the Partner Loan')))
        return res

    _columns = {
        'partner_aml': fields.selection(
            _get_selection_partner_aml,
            'Partner to use',
            help="If this field check with True,\
                it will be create journal entries with\
                partner from partner of employee."),
    }

    _defaults = {
        'partner_aml': 'default',
    }


class hr_payslip_line(osv.osv):

    '''
    Payslip Line
    '''
    _inherit = 'hr.payslip.line'

    def _get_partner_id(self, cr, uid, ids, field_name, arg, context=None):
        res = super(hr_payslip_line, self)._get_partner_id(
            cr, uid, ids, field_name, arg, context=context)
        for p_line in self.browse(cr, uid, ids, context=context):
            if p_line.salary_rule_id.partner_aml == 'default':
                pass
            elif p_line.salary_rule_id.partner_aml == 'loan':
                res[p_line.id] = p_line.loan_line_id.hr_loan_id.partner_id.id
        return res

    _columns = {
        'partner_id': fields.function(
            _get_partner_id,
            type='many2one',
            relation='res.partner',
            string='Partner'),
    }
