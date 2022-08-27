{
    'name': 'Asistencia',
    'version': '1.0',
    'summary': 'Asistencia de refrigerio',
    'description': """
                Registro de asistencia refrigerio.
    """,
    'category': 'Asistencia',
    "author": "CEPHEID",
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['hr_attendance'],
    'data': [
        'views/inherit_views.xml',
        'views/web_asset_backend_template.xml',
    ],

    'qweb': [
        "static/src/xml/attendance.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}