from odoo import models, fields


class OrderOrder(models.Model):
    _name = 'order.order'


class OrderOrderLine(models.Model):
    _name = 'order.order.line'

    order_id = fields.Many2one('order.order', string='Pedido', required=True)
    product_id = fields.Many2one('order.product', string='Producto', required=True)
    quantity = fields.Integer('Cantidad', string='Producto', default=1, required=True)
