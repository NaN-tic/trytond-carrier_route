# This file is part of the carrier_route module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.from trytond.pool import PoolMeta
from trytond.pool import PoolMeta


__all__ = ['Property']
__metaclass__ = PoolMeta


class Property:
    __name__ = 'ir.property'
    _history = True
