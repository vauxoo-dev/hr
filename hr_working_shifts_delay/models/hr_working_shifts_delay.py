<?xml version="1.0" encoding="UTF-8"?>
<openerp>
	<data>

		<record model="ir.ui.view" id="hr_working_shifts_calendar_resources">
			<field name="name">Calendar Resources shifts </field>
			<field name="model">resource.calendar</field>
			<field name="type">form</field>
			<field name="inherit_id" ref="resource.resource_calendar_form"/>
			<field name="arch" type="xml">
				<notebook >
                	<page string="Basic settings">
					</page>
					<page string="Calculation">
					</page>
					<page string="Statistic Items">
					</page>
					<page string="Weekend set">
					</page>										
				</notebook>
            </field>
		</record>

	</data>
</openerp>