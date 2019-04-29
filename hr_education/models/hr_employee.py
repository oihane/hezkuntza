# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    edu_position_ids = fields.Many2many(
        comodel_name='education.position', relation='edu_employee_position',
        column1='employee_id', column2='edu_position_id', string='Positions',
        domain=[('type', '=', 'normal')])
    edu_language_ids = fields.Many2many(
        comodel_name='education.language', relation='edu_employee_language',
        column1='employee_id', column2='edu_language_id', string='Languages')
    edu_level_ids = fields.Many2many(
        comodel_name='education.level', relation='edu_employee_level',
        column1='employee_id', column2='edu_level_id', string='Levels')
    edu_subject_ids = fields.Many2many(
        comodel_name='education.subject', relation='edu_employee_subject',
        column1='employee_id', column2='edu_subject_id', string='Subjects')