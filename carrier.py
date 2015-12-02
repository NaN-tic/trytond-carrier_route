# This file is part of the carrier_route module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool
from trytond.pyson import PYSONEncoder, Eval
from trytond.wizard import Wizard, StateAction
from trytond.transaction import Transaction
from trytond.config import config as config_
from sql import Column
from sql.aggregate import Max
from sql.conditionals import Coalesce
from sql.functions import Trim, Substring

__all__ = ['CarrierRoute', 'CarrierRouteHistory', 'OpenCarrierRouteHistory']
DIGITS = config_.getint('product', 'price_decimal', default=4)


class CarrierRoute(ModelSQL, ModelView):
    'Carrier Route'
    __name__ = 'carrier.route'
    party = fields.Many2One('party.party', 'Party', required=True, select=True)
    cost_price = fields.Property(fields.Numeric('Cost Price',
            digits=(16, DIGITS), required=True))
    from_zip = fields.Char('From Zip')
    from_city = fields.Char('From City')
    from_country = fields.Many2One('country.country', 'From Country')
    from_subdivision = fields.Many2One('country.subdivision',
        'From Subdivision', domain=[
            ('country', '=', Eval('from_country')),
            ], depends=['from_country'])
    to_zip = fields.Char('To Zip')
    to_city = fields.Char('To City')
    to_country = fields.Many2One('country.country', 'To Country')
    to_subdivision = fields.Many2One('country.subdivision',
        'To Subdivision', domain=[
            ('country', '=', Eval('to_country')),
            ], depends=['to_country'])

    def get_rec_name(self, name):
        rec_name = 'From %s to %s by %s' % (
            self.from_city, self.to_city, self.party.rec_name)
        return rec_name


class CarrierRouteHistory(ModelSQL, ModelView):
    'History of Carrier Route'
    __name__ = 'carrier.route_history'
    _rec_name = 'date'
    carrier_route = fields.Many2One('carrier.route', 'Product')
    date = fields.DateTime('Date')
    cost_price = fields.Numeric('Cost Price')

    @classmethod
    def __setup__(cls):
        super(CarrierRouteHistory, cls).__setup__()
        cls._order.insert(0, ('date', 'DESC'))

    @classmethod
    def table_query(cls):
        pool = Pool()
        Property = pool.get('ir.property')
        Field = pool.get('ir.model.field')
        property_history = Property.__table_history__()
        field = Field.__table__()
        return property_history.join(field,
            condition=field.id == property_history.field
            ).select(Max(Column(property_history, '__id')).as_('id'),
                Max(property_history.create_uid).as_('create_uid'),
                Max(property_history.create_date).as_('create_date'),
                Max(property_history.write_uid).as_('write_uid'),
                Max(property_history.write_date).as_('write_date'),
                Coalesce(property_history.write_date,
                    property_history.create_date).as_('date'),
                Trim(Substring(property_history.res, ',.*'), 'LEADING', ','
                    ).cast(cls.carrier_route.sql_type().base)
                    .as_('carrier_route'),
                Trim(property_history.value, 'LEADING', ','
                    ).cast(cls.cost_price.sql_type().base).as_('cost_price'),
                where=(field.name == 'cost_price')
                & property_history.res.like('carrier.route,%'),
                group_by=(property_history.id,
                    Coalesce(property_history.write_date,
                        property_history.create_date),
                    property_history.res, property_history.value))


class OpenCarrierRouteHistory(Wizard):
    'Open Carrier Route History'
    __name__ = 'carrier.route_history.open'
    start_state = 'open'
    open = StateAction('carrier_route.act_carrier_route_history_form')

    def do_open(self, action):
        pool = Pool()
        CarrierRoute = pool.get('carrier.route')

        active_id = Transaction().context.get('active_id')
        if not active_id or active_id < 0:
            action['pyson_domain'] = PYSONEncoder().encode([
                    ('carrier_route', '=', None),
                    ])
        else:
            carrier_route = CarrierRoute(active_id)
            action['pyson_domain'] = PYSONEncoder().encode([
                    ('carrier_route', '=', carrier_route.id),
                    ])
        return action, {}
