
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
from src.client_data.client_data import parse_client_document

class ClientData_test(unittest.TestCase):

	def test_parse_raw_location(self):
		# assert ValueError
		self.assertRaises(ValueError, parse_raw_location, 'a33.13091', '43.51828')

		# assert long,lat assignment
		location = parse_raw_location('33.13091', '43.51828')
		assert (location[0] == 43.51828) and (location[1] == 33.13091)

	def test_parse_client_document(self):
		# assert for incorrect number of fragments
		self.assertRaises(ValueError, parse_client_document, '')

		# assert correct fragment assignement
		line = '26000:1329519:Joseph Asoofi KSFO:PILOT::33.13091:43.51828:38318:465:H/B703:495:OMDB:38000:EGSS:USA-E:100:1:1200:::1:I:0:0:6:24:7:40:EGGW: /r/:NADI2F NADIL M557 BALUS UL768 RAMSI UL602 RALKA G795 TASMI UL602 DRZ UM861 BUK UL602 MAKOL L602 KOMAN UL602 TIXIP UY553 DEGET DCT ABETI UL610 BATTY UL608 COA UL179 SASKI UL608 SUMUM UY6 IDESI CASE1C:0:0:0:0:::20170531163452:297:29.822:1009:'
		document = {}
		document['callsign'] = '26000'
		document['cid'] = '1329519'
		document['realname'] = 'Joseph Asoofi KSFO'
		document['client_type'] = 'PILOT'
		document['location'] = [43.51828, 33.13091]
		document['altitude'] = 38318
		document['groundspeed'] = 465
		document['heading'] = 297
		document['flight_rules'] = 'I'
		document['departure_ICAO'] = 'OMDB'
		document['destination_ICAO'] = 'EGSS'
		document['alternate_ICAO'] = 'EGGW'
		document['requested_flight_level'] = 38000
		document['route'] = 'NADI2F NADIL M557 BALUS UL768 RAMSI UL602 RALKA G795 TASMI UL602 DRZ UM861 BUK UL602 MAKOL L602 KOMAN UL602 TIXIP UY553 DEGET DCT ABETI UL610 BATTY UL608 COA UL179 SASKI UL608 SUMUM UY6 IDESI CASE1C'
		document['remarks'] = ' /r/'
		document['aircraft'] = 'H/B703'

		self.assertEqual(parse_client_document(line), document)