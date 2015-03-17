# coding=utf-8

#    Copyright (C) 2012-2013  Federico Manuel Echeverri Choux
#    Vauxoo - http://www.vauxoo.com  :  echeverrifm@vauxoo.com
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#! /usr/bin/python


from openerp import models, fields, api, _


class hr_working_shifts_delay (models.Model):

    _inherit = 'resource.calendar'

    one_workday_as = fields.Integer(string='One workday as', help="")
    least_min = fields.Integer(string='Least minutes of shift inteval (mins)', help="Least minutes of shift inteval (mins)")
    min_as_late = fields.Integer(string='Clock-in over mins count as later ( min )', help="Clock-in over mins count as later")
    min_as_early = fields.Integer(string='Clock-out over mins count as early ( min )', help="Clock-out over mins count as early")
    noclockin_count_as = fields.Selection([('late','Late'), ('absent','Absent')],string='If no clock in, count as ( min )', required=True, default='late')
    noclockin_count_mins = fields.Integer(string='If no clock in (min)', help="", default=60)
    noclockout_count_as = fields.Selection([('early','Early Leave'), ('absent','Absent')],string='If no clock out, count as ( min )', required=True, default='early')
    noclockout_count_mins = fields.Integer(string='If no clock out (min)', help="", default=60)
    as_late_exceed = fields.Integer(string='As late exceed', help="")
    as_early_leave = fields.Integer(string='As early leave', help="")
    inter_leaving_ot = fields.Integer(string='Interval of leaving count as OT', help="")
    checkout_interval_ot = fields.Integer(string='This interval count as OT', help="")
    ot_after_checkout = fields.Integer(string='The longest over time after check out', help="")
    checkin_count_ot = fields.Integer(string='Interval of check-in count as OT', help="")
    checkin_interval_ot = fields.Integer(string='This interval count as OT', help="")
    ot_defore_checkin = fields.Integer(string='The longest over time before check-in', help="")
    longest_over_time = fields.Integer(string='The longest over time', help="")

