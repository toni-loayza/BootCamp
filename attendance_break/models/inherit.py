from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_break = fields.Datetime('Entrada Refrigerio')
    check_out_break = fields.Datetime('Salida Refrigerio')

    # is_saturday = fields.Boolean('Es sabado', default=False)

    @api.depends('check_in', 'check_in_break', 'check_out_break', 'check_out')
    def _compute_worked_hours(self):
        res = super(HrAttendance, self)._compute_worked_hours()
        for attendance in self:
            # if attendance.is_saturday:
            #     if attendance.check_out and attendance.check_in and not attendance.check_out_break and not attendance.check_in_break:
            #         delta = attendance.check_out - attendance.check_in
            #         attendance.worked_hours = delta.total_seconds() / 3600.0
            #     else:
            #         attendance.worked_hours = False
            # else:
            if attendance.check_out and attendance.check_in and attendance.check_out_break and attendance.check_in_break:
                delta = attendance.check_out - attendance.check_in
                delta_break = attendance.check_out_break - attendance.check_in_break
                descu_break = delta - delta_break
                attendance.worked_hours = descu_break.total_seconds() / 3600.0
            else:
                # attendance.worked_hours = False
                attendance.worked_hours = False
        return res

    # @api.constrains('check_in')
    # def constraint_check_in(self):
    #     check_in = self.env['hr.attendance'].search([
    #         ('employee_id', '=', self.employee_id.id),
    #         ('id', '!=', self.id)])
    #     for x in check_in:
    #         if x.check_in.strftime('%Y-%m-%d') == self.check_in.strftime('%Y-%m-%d'):
    #             raise UserError(_("Un usuario no puede registrar dos horarios en el mismo día"))


# class HolidaysRequest(models.Model):
#     _inherit = "hr.leave"
#
#     attach_document = fields.Binary(tracking=True, string='Adjuntar evidencia')
#
#     @api.constrains('name')
#     def constrains_name_len(self):
#         if len(self.name) > 500:
#             contado = len(self.name)
#             diferencia = 500 - contado
#             raise UserError(
#                 _("El numero de caracteres maximo permitidos es de 500, estas superando por %s.") % diferencia)


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    # attendance_state = fields.Selection(string="Attendance Status", compute='_compute_attendance_state',
    #                                     selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")])
    attendance_state = fields.Selection(selection_add=[('Ingreso_Refrigerio', 'Ingreso Refigerio'),
                                                       ('Salida_Refrigerio', 'Salida Refrigerio')],
                                        default='checked_out')

    # is_saturday = fields.Boolean('Es sabado', default=False, compute='_compute_attendance_state', store=True)

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_state(self):
        res = super(HrEmployeeBase, self)._compute_attendance_state()
        for employee in self:
            # if datetime.today().isoweekday() == 6:
            #     self.is_saturday = True
            # else:
            #     self.is_saturday = False

            att = employee.last_attendance_id.sudo()
            # employee.attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'
            # if employee.is_saturday:
            #     if att.check_in and not att.check_in_break and not att.check_out_break and not att.check_out:
            #         employee.attendance_state = 'checked_in'
            #     else:
            #         employee.attendance_state = 'checked_out'
            # else:
            if att.check_in and not att.check_in_break and not att.check_out_break and not att.check_out:
                employee.attendance_state = 'Ingreso_Refrigerio'
            elif att.check_in and att.check_in_break and not att.check_out_break and not att.check_out:
                employee.attendance_state = 'Salida_Refrigerio'
            elif att.check_in and att.check_in_break and att.check_out_break and not att.check_out:
                employee.attendance_state = 'checked_in'
            else:
                employee.attendance_state = 'checked_out'
            print('estado asistencia', employee.attendance_state)
        return res

    # def attendance_manual(self, next_action, entered_pin=None):
    #     self.ensure_one()
    #     can_check_without_pin = not self.env.user.has_group('hr_attendance.group_hr_attendance_use_pin') or (
    #             self.user_id == self.env.user and entered_pin is None)
    #     if can_check_without_pin or entered_pin is not None and entered_pin == self.sudo().pin:
    #         return self._attendance_action(next_action)
    #     return {'warning': _('Wrong PIN')}
    #
    # def _attendance_action(self, next_action):
    #     self.ensure_one()
    #     employee = self.sudo()
    #     action_message = self.env["ir.actions.actions"]._for_xml_id(
    #         "hr_attendance.hr_attendance_action_greeting_message")
    #     action_message['previous_attendance_change_date'] = employee.last_attendance_id and (
    #             employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
    #     action_message['employee_name'] = employee.name
    #     action_message['barcode'] = employee.barcode
    #     action_message['next_action'] = next_action
    #     action_message['hours_today'] = employee.hours_today
    #
    #     if employee.user_id:
    #         modified_attendance = employee.with_user(employee.user_id)._attendance_action_change()
    #     else:
    #         modified_attendance = employee._attendance_action_change()
    #     action_message['attendance'] = modified_attendance.read()[0]
    #     return {'action': action_message}

    def _attendance_action_change(self):
        self.ensure_one()
        action_date = fields.Datetime.now()
        # if not self.is_saturday:
        if self.attendance_state == 'checked_out':
            print("out_fin")
            return super(HrEmployeeBase, self)._attendance_action_change()
            # vals = {
            #     'employee_id': self.id,
            #     'check_in': action_date,
            # }
            # return self.env['hr.attendance'].create(vals)
        # attendance = ""
        if self.attendance_state == 'Ingreso_Refrigerio':
            print("ingre_ref")
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id),
                                                           ('check_in_break', '=', False),
                                                           ('check_out_break', '=', False),
                                                           ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_in_break = action_date
            else:
                raise exceptions.UserError(
                    _('No se puede realizar el check-out en %(empl_name)s, no se pudo encontrar el ingreso de refigerio'
                      ' correspondiente.'
                      'Sus asistencias probablemente han sido modificadas manualmente por recursos humanos.') % {
                        'empl_name': self.sudo().name, })
            return attendance
        if self.attendance_state == 'Salida_Refrigerio':
            print("sali_ref")
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id),
                                                           ('check_out_break', '=', False),
                                                           ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out_break = action_date
            else:
                raise exceptions.UserError(
                    _('No se puede realizar el check-out en %(empl_name)s, no se pudo encontrar la salida de refrigerio'
                      ' correspondiente.'
                      'Sus asistencias probablemente han sido modificadas manualmente por recursos humanos.') % {
                        'empl_name': self.sudo().name, })
            return attendance
        if self.attendance_state == 'checked_in':
            print("ingre_inicio")
            return super(HrEmployeeBase, self)._attendance_action_change()
            # attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id),
            #                                                ('check_out', '=', False)], limit=1)
            # if attendance:
            #     attendance.check_out = action_date
            # else:
            #     raise exceptions.UserError(
            #         _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
            #           'Your attendances have probably been modified manually by human resources.') % {
            #             'empl_name': self.sudo().name, })
            # return attendance
    # else:
    #     if self.attendance_state == 'checked_out':
    #         vals = {
    #             'employee_id': self.id,
    #             'check_in': action_date,
    #             'is_saturday': True,
    #         }
    #         return self.env['hr.attendance'].create(vals)
    #     # attendance = ""
    #     if self.attendance_state == 'checked_in':
    #         attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id),
    #                                                        ('check_in_break', '=', False),
    #                                                        ('check_out_break', '=', False),
    #                                                        ('check_out', '=', False)], limit=1)
    #         if attendance:
    #             attendance.check_out = action_date
    #         else:
    #             raise exceptions.UserError(
    #                 _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
    #                   'Your attendances have probably been modified manually by human resources.') % {
    #                     'empl_name': self.sudo().name, })
    #         return attendance
