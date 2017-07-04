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
def parse_raw_location(latitude, longitude):
	"""Groups decimal latitude and longitude values into a `location` list

    Args:
        latitude (float): Decimal latitude, type float or parseable from string.
        longitude (float): The second parameter, type float or parseable from string.

    Returns:
        list: [`longitude`, `latitude`]
	"""
	# As per GEOJson Spec (RFC 7946) location coordinates are ordered longitude,latitude
	return [ float(longitude), float(latitude) ]

def parse_client_document(line):
	"""Parses a line from VATSIM status data's CLIENTS section into a client document

	Args:
		line (string): A single line from VATSIM status data's CLIENTS section
	"""
	# split line into fragments
	line = line.strip()
	fragments = line.split(':')

	# verify we have the correct number of fragments
	if len(fragments) != 42: raise ValueError('Incorrect number of fragments in line.')

	# assign fragments
	# make sure on int we correctly filter out empty values ont integers parsing
	document = {}
	document['callsign'] = fragments[0]
	document['cid'] = fragments[1]
	document['realname'] = fragments[2]
	document['client_type'] = fragments[3]
	document['location'] = parse_raw_location(fragments[5], fragments[6])
	document['altitude'] = int(fragments[7]) if fragments[7] != '' else 0
	document['groundspeed'] = int(fragments[8]) if fragments[8] != '' else 0
	document['heading'] = int(fragments[38]) if fragments[38] != '' else 0
	document['flight_rules'] = fragments[21]
	document['departure_ICAO'] = fragments[11]
	document['destination_ICAO'] = fragments[13]
	document['alternate_ICAO'] = fragments[28]
	document['requested_flight_level'] = fragments[12]
	document['route'] = fragments[30]
	document['remarks'] = fragments[29]
	document['aircraft'] = fragments[9]

	return document