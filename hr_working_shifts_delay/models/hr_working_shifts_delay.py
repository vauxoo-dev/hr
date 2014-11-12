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


from openerp.osv import fields, orm

class hr_working_shifts_delay (orm.Model):

    _inherit = ['resource.calendar']
    _columns = {
    		'one_workday_as': fields.integer('One workday as', help=""),
            'least_min': fields.integer('Least minutes of shift inteval (mins)', help="Least minutes of shift inteval (mins)"),
            'min_as_late': fields.integer('Clock-in over mins count as later ( min )', help="Clock-in over mins count as later"),
            'min_as_early': fields.integer('Clock-out over mins count as early ( min )', help="Clock-out over mins count as early"),
            'noclockin_count_as': fields.selection([('late','Late'), ('absent','Absent')],'If no clock in, count as ( min )', required=True),
            'noclockin_count_mins': fields.integer('If no clock in (min)', help=""),
            'noclockout_count_as': fields.selection([('early','Early Leave'), ('absent','Absent')],'If no clock out, count as ( min )', required=True),
            'noclockout_count_mins': fields.integer('If no clock out (min)', help=""),
            'as_late_exceed': fields.integer('As late exceed', help=""),
            'as_early_leave': fields.integer('As early leave', help=""),
            'inter_leaving_ot': fields.integer('Interval of leaving count as OT', help=""),
            'checkout_interval_ot': fields.integer('This interval count as OT', help=""),
            'ot_after_checkout': fields.integer('The longest over time after check out', help=""),
            'checkin_count_ot': fields.integer('Interval of check-in count as OT', help=""),
            'checkin_interval_ot': fields.integer('This interval count as OT', help=""),
            'ot_defore_checkin': fields.integer('The longest over time before check-in', help=""),
            'longest_over_time': fields.integer('The longest over time', help=""),
    }

    _defautls = {
    		'noclockin_count_as': 'late',
    		'noclockin_count_mins': 60,
    		'noclockout_count_as': 'early',
    		'noclockout_count_mins': 60,
    }

