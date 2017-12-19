#!/usr/bin/env python
"""
VATSIM Status Proxy
Copyright (C) 2017  Pedro Rodrigues <prodrigues1990@gmail.com>

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
from ddt import ddt, unpack, file_data, data
from src import icao_data

@ddt
class IcaoDataTests(unittest.TestCase):

    def setUp(self):
        self.api_url = 'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/airspaces/zones/fir-list'
        self.api_key = ''

    def test_import_data(self):
        icao_data.import_data(self.api_url, self.api_key)

    def test_request_icao_data(self):
        self.assertEqual(icao_data.request_icao_data(
                self.api_url,
                self.api_key).status_code, # API key
            200)
