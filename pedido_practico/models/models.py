from odoo import models, fields


class Customers(models.Model):
    _name = 'order.customers'
    _description = 'Cliente'

    document = fields.Char('Documento de indentidad', required=True, size=8)
    name = fields.Char('Apellidos y Nombres', required=True, size=100)
    phone = fields.Char('Telefono', size=9)
    address_ids = fields.One2many('order.customers.address', 'customers_id', string='Direcciones')


class Address(models.Model):
    _name = 'order.customers.address'
    _description = 'Direcciones del cliente'

    customers_id = fields.Many2one('order.customers', string='Cliente')
    name = fields.Char('Lugar', required=True,)
    address = fields.Char('Dirección', required=True,)

    def name_get(self):
        result = []
        for rec in self:
            name = '{} ({})'.format(rec.name, rec.address)
            result.append((rec.id, name))
        return result
