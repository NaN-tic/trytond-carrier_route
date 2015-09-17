# This file is part of the carrier_route module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .ir import *
from .carrier import *

def register():
    Pool.register(
        Property,
        CarrierRoute,
        CarrierRouteHistory,
        module='carrier_route', type_='model')
    Pool.register(
        OpenCarrierRouteHistory,
        module='carrier_route', type_='wizard')
