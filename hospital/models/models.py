from odoo import fields, models

TIPO_DOC_SELECCION = [
    ('01', u'DNI'),
    ('03', u'Carnet Extranjería'),
    ('06', u'Pasaporte')
]


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Modelo Hospital Paciente'

    tipo_documento = fields.Selection(TIPO_DOC_SELECCION, 'Tipo de documento', default='01', required=True)
    numero_documento = fields.Char('Numero de documento', required=True, size=12, index=True)
    apellido_paterno = fields.Char('Apellido paterno', required=True, size=100)
    apellido_materno = fields.Char('Numero de documento', required=True, size=100)
    nombres = fields.Char('Nombres', required=True, size=100)
