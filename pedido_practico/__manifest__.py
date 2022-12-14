{
    'name': 'Pedido de comida',
    'version': '1.0',
    'category': 'pedido',
    'summary': 'Pedidos de comida por internet',
    'website': 'https://escuelafullstack.com/',
    'depends': [
        'mail'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/models_views.xml',
        'views/order_order_views.xml',
        'views/order_product_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}