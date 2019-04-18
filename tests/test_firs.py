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

class FirsTest(unittest.TestCase):
    """Tests for VatsimStatus dataclass."""
    def test(self):
        """Test against a sample version of the status information."""
        with open('VATSpy.dat', 'r', errors='ignore') as file:
            file = file.readlines()
        status = Firs(file)

        self.assertTrue(len(status.firs) > 0)
        self.assertTrue(len(status.uirs) > 0)
        self.assertTrue(len(status.airports) > 0)
        for item in [*status.firs, *status.uirs, *status.airports]:
            self.assertIs(type(item), dict)
