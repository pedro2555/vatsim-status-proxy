
#!/usr/bin/env python
"""
VATSIM Status Proxy.
Copyright (C) 2017  Pedro Rodrigues <prodrigues1990@gmail.com>

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
from src.client_data.client_data import parse_raw_location

class ClientData_test(unittest.TestCase):
	def test_parse_raw_location(self):
		location = parse_raw_location('33.13091', '43.51828')
		assert (location[0] == 43.51828) and (location[1] == 33.13091)

		self.assertRaises(ValueError, parse_raw_location, 'a33.13091', '43.51828')