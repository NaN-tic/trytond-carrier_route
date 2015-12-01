# This file is part of the carrier_route module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CarrierRouteTestCase(ModuleTestCase):
    'Test Carrier Route module'
    module = 'carrier_route'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CarrierRouteTestCase))
    return suite