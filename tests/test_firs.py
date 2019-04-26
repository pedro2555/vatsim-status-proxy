"""
VATSIM Status Proxy
Copyright (C) 2017 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

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

from src.firs import Firs
from src.firs_polygons import FirsPolygons

class FirsTest(unittest.TestCase):
    """Tests for VatsimStatus dataclass."""
    def test_firs_info(self):
        """Test against a sample version of the status information."""
        with open('VATSpy.dat', 'r', errors='ignore') as file:
            file = file.read()
        status = Firs(file)

        for item in [*status.firs, *status.uirs, *status.airports]:
            self.assertIs(type(item), dict)
        self.assertTrue(len(status.airports) > 0)
        self.assertTrue(len(status.firs) > 0)
        self.assertTrue(len(status.uirs) > 0)

    def test_firs_polygons(self):
        """Test against a sample version of the status information."""
        with open('FIRBoundaries.dat', 'r', errors='ignore') as file:
            file = file.readlines()
        status = FirsPolygons(file)

        for item in [*status.firs_polygons]:
            self.assertIs(type(item), str)
        self.assertTrue(len(status.firs_polygons) > 0)
