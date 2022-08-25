import dateutil.relativedelta

from odoo import fields


def get_edad(fecha_1, fecha_2=False, record=False):
    """Devuelve relativedelta entre las fechas
    :param str fecha_1: Fecha Inicio
    :param str fecha_2: Fecha Final (opcional)
    :param record: record de odoo(self) obligatorio si fecha dos es False
    :return_type: relativedelta
    """
    if not fecha_2:
        fecha_2 = fecha_2 or fields.Date.context_today(record)

    fecha_1 = fecha_1 and fields.Datetime.from_string(fecha_1)
    fecha_2 = fecha_2 and fields.Datetime.from_string(fecha_2)
    delta = fecha_1 and fecha_2 and (fecha_2 - fecha_1)
    return delta and dateutil.relativedelta.relativedelta(fecha_2, fecha_1)


def calculo_dias(fecha_1, fecha_2=False, record=False):
    """Devuelve cadena con la edad en años, meses y días
    :param str fecha_1: Fecha Inicio
    :param str fecha_2: Fecha Final (opcional)
    :param record: record de odoo(self) obligatorio si fecha dos es False
    :return_type: str
    """

    age = get_edad(fecha_1, fecha_2, record)
    if not age:
        return '0 días'

    if age.years:
        return u'{} años {} meses {} días'.format(age.years, age.months, age.days)
    else:
        if age.months:
            return u'{} meses {} días'.format(age.months, age.days)
        else:
            return u'{} días'.format(age.days)
