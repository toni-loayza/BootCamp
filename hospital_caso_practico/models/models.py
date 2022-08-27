from odoo import fields, models, api
from ..services.utils import (calculo_dias)

TIPO_DOC_SELECCION = [
    ('01', u'DNI'),
    ('03', u'Carnet Extranjería'),
    ('06', u'Pasaporte')
]


class HospitalPatient(models.Model):
    _name = 'hospital.patient.practica'
    _description = 'Modelo Hospital Paciente'

    tipo_documento = fields.Selection(TIPO_DOC_SELECCION, 'Tipo de documento', default='01', required=True)
    numero_documento = fields.Char('Numero de documento', required=True, size=12, index=True)
    apellido_paterno = fields.Char('Apellido paterno', required=True, size=100)
    apellido_materno = fields.Char('Apellido materno', required=True, size=100)
    nombres = fields.Char('Nombres', required=True, size=100)
    #segunda parte
    name = fields.Char('Apellidos y Nombres', compute='compute_name', store=True)
    fecha_nacimiento = fields.Date('Fecha de nacimiento')
    edad = fields.Char('Edad', compute='compute_edad')

    @api.depends('apellido_paterno', 'apellido_materno', 'nombres')
    def compute_name(self):
        # primero de segunda
        # self.name = '{} {} {}'.format(self.apellido_paterno, self.apellido_materno, self.nombres)

        # segundo de segunda
        # for rec in self:
        #     rec.name = '{} {} {}'.format(rec.apellido_paterno, rec.apellido_materno, rec.nombres)

        for rec in self:
            if rec.apellido_paterno and rec.apellido_materno and rec.nombres:
                rec.name = '{} {} {}'.format(rec.apellido_paterno, rec.apellido_materno, rec.nombres)

    @api.depends('fecha_nacimiento')
    def compute_edad(self):
        for rec in self:
            if rec.fecha_nacimiento:
                rec.edad = calculo_dias(rec.fecha_nacimiento, False, self)
            else:
                rec.edad = False
