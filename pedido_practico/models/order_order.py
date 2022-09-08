from odoo import models, fields, api

STATUS_OPTIONS = [
    ('registro', 'Registro'),
    ('preparando', 'En preparación'),
    ('finalizado', 'Finalizado')
]

class OrderOrder(models.Model):
    _name = 'order.order'
    _inherit = 'mail.thread'
    _description = 'Pedido'
    _rec_name = 'customers_id'

    line_ids = fields.One2many('order.order.line', 'order_id', string='Detalles')
    # hora estatica
    # date = fields.Date(string='Fecha del pedido', default=fields.Date.today())

    # hora cambiante pero no con la zona horaria de odoo
    # date = fields.Date(string='Fecha del pedido', default=lambda self: fields.Date.today())

    # esta si "cerrar sesion para que funcione"
    date = fields.Date(string='Fecha del pedido', default=lambda self: fields.Date.context_today(self))
    customers_id = fields.Many2one('order.customers', string='Cliente')
    address_id = fields.Many2one('order.customers.address', string='Direccion de entrega', tracking=True)
    state = fields.Selection(STATUS_OPTIONS, string='Estado', default='registro', tracking=True)

    @api.onchange('customers_id')
    def onchange_customers(self):
        self.address_id = False
        if len(self.customers_id.address_ids) == 1:
            self.address_id = self.customers_id.address_ids

    def action_setup(self):
        self.write({'state': 'preparando'})
        for line in self.line_ids:
            line.product_id.sudo().write({'stock': line.product_id.stock - line.quantity})

    def action_finalize(self):
        self.write({'state': 'finalizado'})


class OrderOrderLine(models.Model):
    _name = 'order.order.line'
    _description = 'Detalle Pedido'

    order_id = fields.Many2one('order.order', string='Pedido', required=True)
    product_id = fields.Many2one('order.product', string='Producto', required=True, domain=[('stock', '>', 0)],)
    quantity = fields.Integer('Cantidad', default=1, required=True)
    unit_price = fields.Float(related='product_id.price')
    subtotal = fields.Float(string='Subtotal', compute='compute_subtotal')

    @api.depends('product_id', 'unit_price')
    def compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price * (1 - rec.product_id.discount / 100)
