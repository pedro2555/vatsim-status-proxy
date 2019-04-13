
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
from ddt import ddt, unpack, file_data, data
from datetime import datetime
from src import vatsim_data

@ddt
class VatsimDataTests(unittest.TestCase):

	def test_match_spec_token(self):
		# no match should return None
		self.assertEqual(vatsim_data._match_spec_token('', 'spec_token'), None)

		# returns matched name
		self.assertEqual(vatsim_data._match_spec_token('; !CLIENTS section -   test', 'spec_token'), 'clients')

	@file_data('test_assign_from_spec.json')
	def test_assign_from_spec(self, spec, lines):
		for line in lines:
			result = vatsim_data._assign_from_spec(
				spec,
				line,
				{
			        'callsign': str,
			    	'cid': str,
			    	'realname': str,
			    	'clienttype': str,
			    	'groundspeed': int,
			    	'altitude': int
			    })

			# check id fragments, location is only parsed by _convert_latlong_to_geojson
			for spec_fragment in 'callsign:cid:realname:clienttype'.split(':'):
				if spec_fragment != 'latitude' and spec_fragment != 'longitude':
					self.assertIn(spec_fragment, result)

			# check no invalid or empty values
			self.assertNotIn('', result)
			self.assertIsInstance(result['callsign'], str)
			self.assertIsInstance(result['cid'], str)
			self.assertIsInstance(result['realname'], str)
			self.assertIsInstance(result['clienttype'], str)
			if 'groundspeed' in result:
				self.assertIsInstance(result['groundspeed'], int)
			if 'altitude' in result:
				self.assertIsInstance(result['altitude'], int)

	@file_data('test_convert_latlong_to_geojson.json')
	def test_convert_latlong_to_geojson(self, test, location_key):
		new_dict = vatsim_data._convert_latlong_to_geojson(test)

		self.assertIn(location_key, new_dict)

	def test_parse_updated_datetime(self):
		subject = '; Created at 31/05/2017 21:11:08 UTC by Data Server V4.0'
		test = datetime(2017, 5, 31, 21, 11, 8, 0)

		self.assertEqual(vatsim_data._parse_updated_datetime(subject), test)
