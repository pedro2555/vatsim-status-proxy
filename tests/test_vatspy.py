"""
VATSIM Status Proxy
Copyright (C) 2017 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>
                           Tiago Vicente <tmavicente@gmail.com>

This file is part of VATSIM Status Proxy.

VATSIM Status Proxy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

VATSIM Status Proxy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VATSIM Status Proxy.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest

from src.vatspy import VatspyDat

class VatspyTest(unittest.TestCase):
    """Tests for Vatspy dataclasses."""
    def test_dat(self):
        """Test against a sample version of the VATspy.dat information."""
        with open('VATSpy.dat', 'r', errors='ignore') as file:
            file = file.readlines()
        status = VatspyDat(file)

        for item in [*status.countries, *status.airports, *status.firs, *status.uirs, *status.idl]:
            self.assertIs(type(item), dict)
        # countries
        self.assertTrue(len(status.countries) > 0)
        for country in status.countries:
            self.assertEqual(len(country), 3, country)
        # airports
        self.assertTrue(len(status.airports) > 0)
        for airport in status.airports:
            self.assertEqual(len(airport), 7, airport)
        # firs
        self.assertTrue(len(status.firs) > 0)
        for fir in status.firs:
            self.assertEqual(len(fir), 4, fir)
        # uirs
        self.assertTrue(len(status.uirs) > 0)
        for uir in status.uirs:
            self.assertEqual(len(uir), 3, uir)
        # idl
        self.assertTrue(len(status.idl) > 0)
        for _idl in status.idl:
            self.assertEqual(len(_idl), 2, _idl)
