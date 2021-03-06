# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models
from psycopg2.extensions import AsIs


class EducationGroupStudentTimetableReport(models.Model):
    _name = 'education.group.student.timetable.report'
    _inherit = 'education.group.student.report'
    _description = 'Student Timetable Report'
    _auto = False
    _rec_name = 'student_id'
    _order = 'academic_year_id, dayofweek, hour_from, hour_to'

    def _get_selection_dayofweek(self):
        return self.env['resource.calendar.attendance'].fields_get(
            allfields=['dayofweek'])['dayofweek']['selection']

    dayofweek = fields.Selection(
        selection='_get_selection_dayofweek', string='Day of Week')
    daily_hour = fields.Integer(string="Hour in Day")
    hour_from = fields.Float(string='Work from', group_operator="min")
    hour_to = fields.Float(string='Work to', group_operator="max")
    professor_id = fields.Many2one(
        comodel_name='hr.employee', string='Teacher')

    _depends = {
        'education.schedule': [
            'subject_id', 'classroom_id', 'teacher_id', 'academic_year_id'
        ],
        'education.group': [
            'center_id', 'course_id', 'student_ids'
        ],
        'education.schedule.timetable': [
            'dayofweek', 'session_number', 'hour_to', 'hour_from',
            'subject_name'
        ]
    }

    def _coalesce(self):
        coalesce_str = """
            , COALESCE(sch_tt.teacher_id, sch.teacher_id) AS professor_id
            , COALESCE(sch_tt.subject_name, sub_name.name, sbt.description,
                       tt.description, 'undefined') AS subject_name
        """
        return coalesce_str

    def _select(self):
        select_str = """
                , cal_att.dayofweek AS dayofweek,
                sch_tt.session_number AS daily_hour,
                cal_att.hour_from AS hour_from,
                cal_att.hour_to AS hour_to
        """
        return (super(EducationGroupStudentTimetableReport, self)._select() +
                select_str)

    def _from(self):
        from_str = """
                JOIN education_schedule_timetable sch_tt
                  ON sch.id = sch_tt.schedule_id
                JOIN resource_calendar_attendance cal_att
                  ON sch_tt.attendance_id = cal_att.id
        """
        return (super(EducationGroupStudentTimetableReport, self)._from() +
                from_str)

    def _group_by(self):
        group_by_str = """
                , cal_att.dayofweek,
                sch_tt.session_number,
                cal_att.hour_from,
                cal_att.hour_to,
                sch_tt.subject_name,
                sch_tt.teacher_id
        """
        return (super(EducationGroupStudentTimetableReport, self)._group_by() +
                group_by_str)

    @api.model_cr
    def init(self):
        # self._table = education_group_student_timetable_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()),
                AsIs(self._coalesce()), AsIs(self._from()),
                AsIs(self._group_by()),))
