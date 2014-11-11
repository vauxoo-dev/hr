# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Conectel (info@vauxoo.com)
############################################################################
#    Coded by: echeverrifm (echeverrifm@vauxoo.com)
############################################################################
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
##############################################################################

{
    "name" : "hr working shifts delay",
    "version" : "1.0",
    "author" : "Conectel ( Federico Manuel Echeverri Choux ) ",
    "category" : "",
    "description" : """    """,
    "website" : "http://www.conectel.mx/",
    "license" : "AGPL-3",
    "depends" : [
            "base",
            "hr",
            "hr_attendance",
            "hr_attendance_zk",
            "hr_contact",
        ],
    "demo" : [],
    "data" : [
            "hr_working_shifts_delay_view.xml",

    ],
    "installable" : True,
    "active" : False,
}
