from odoo import models, fields


class Customers(models.Model):
    _name = 'pedido.cliente.practica'
    _description = 'Cliente'

    name = fields.Char('Apellidos y Nombres', required=True)
    phone = fields.Char('Telefono')


class Address(models.Model):
    _name = 'pedido.cliente.direccion'
    _description = 'Direcciones del cliente'

    customers_id = fields.Many2one('pedido.cliente', string='Cliente')
    name = fields.Char('Lugar')
    address = fields.Char('Dirección')
