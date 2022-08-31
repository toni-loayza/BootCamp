from odoo import models, fields


class OrderOrder(models.Model):
    _name = 'order.order'

    line_ids = fields.One2many('order.order.line', 'order_id', string='Detalles')
    date = fields.Date(string='Fecha del pedido')


class OrderOrderLine(models.Model):
    _name = 'order.order.line'

    order_id = fields.Many2one('order.order', string='Pedido', required=True)
    product_id = fields.Many2one('order.product', string='Producto', required=True)
    quantity = fields.Integer('Cantidad', default=1, required=True)
