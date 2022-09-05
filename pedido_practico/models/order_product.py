from odoo import models, fields


class OrderProduct(models.Model):
    _name = 'order.product'

    name = fields.Char('Nombre del producto', required=True, size=100)
    stock = fields.Integer('Stock')
    price = fields.Float('Precio')
    discount = fields.Float('Descuento %')
