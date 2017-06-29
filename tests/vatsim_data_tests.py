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
from src import vatsim_data

@ddt
class VatsimDataTests(unittest.TestCase):

	@file_data('test_assign_from_spec.json')
	def test_assign_from_spec(self, spec, lines):
		for line in lines:
			result = vatsim_data.assign_from_spec(spec, line)

			# check all fragments but lat and long
			for spec_fragment in spec.split(':'):
				if spec_fragment != 'latitude' and spec_fragment != 'longitude':
					self.assertIn(spec_fragment, result)

			# check location was inserted
			if 'latitude' in spec and 'longitude' in spec:
				self.assertIn('location', result)
