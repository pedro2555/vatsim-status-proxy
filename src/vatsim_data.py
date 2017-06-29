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
import urllib2
import datetime
import pytz
import re

def assign_from_spec(spec, line):
	"""Returns a dictionary by iterating colon separated values in both spec and line, like
	dictionary[spec] = line.

	Args:
		spec:	(string) colon separated list of spec headers
		line:	(string) colon separated list of values matching spec headers

	Returns:	(dict) A dictionary of spec,line colon separated values
	"""
	spec_fragments = spec.split(':')
	line_fragments = line.split(':')

	if len(spec_fragments) != len(line_fragments):
		raise ValueError('spec fragments do not match line fragments (%s %s)' % spec, line)
	
	result = {}
	for spec_fragment, line_fragment in zip(spec_fragments, line_fragments):
		result[spec_fragment] = line_fragment

	return result

def fix_locations(obj):
	"""Changes any matching lat,long entries into a single GEOJson entry.
	`obj` is expected to have none or more keys that matches `^(?P<start>.*)lon(?P<end>g|.*)$` and
	an equivalent latitude defined by `$start + lat + $end[1:]`.

	Args:
		obj:	(dict) the dictionary to mutate

	Returns:	(dict) the mutated dictionary
	"""
	# search for longitude entries
	new_object = obj
	for key, value in obj.items():
		match = re.match('^(?P<start>.*)lon(?P<end>g|.*)$', key)
		if not match:
			continue

		# if we have a match, locate corresponding latitude
		# 	latitude key should be similiar to longitude
		#	even if matches are empty (ie.: 'longitude') the regex and concatenation bellow should
		#	work ok.
		# disconsider first letter from second match group (this maybe an issue, since it is a bind
		# decision)
		latitude_key = match.groups()[0] + 'lat' + match.groups()[1][1:]
		if latitude_key not in obj:
			continue

		# we can already append the new location, and remove redundant entries in result object
		new_object[match.groups()[0] + 'location'] = [float(value), float(obj[latitude_key])]
		del new_object[key]
		del new_object[latitude_key]

	return new_object

def last_data_server_timestamp(app):
	clients = app.data.driver.db['clients']

	if clients.count() < 1:
		return None

	# get the most outdated client stamp
	# (also remove any timezone information, we'll deal with UTC time only)
	return clients.find().sort('_updated', -1).limit(1)[0]['_updated'].replace(tzinfo=None)

def assign_client_data(line):
	cross_reference = [
		('callsign', 0),
		('cid', 1),
		('client_type', 3),
		('realname', 2),
		('latitude', 5),
		('longitude', 6),
		('altitude', 7),
		('groundspeed', 8),
		('heading', 38),
		('flight_rules', 21),
		('departure_ICAO', 11),
		('destination_ICAO', 13),
		('alternate_ICAO', 28),
		('requested_flight_level', 12),
		('requested_speed', 10),
		('route', 30),
		('remarks', 29),
		('aircraft', 9)
	]

	client_data = {}

	fragments = line.split(':')
	for reference, index in cross_reference:
		client_data[reference] = fragments[index]

def get_VATSIM_clients(eve_app):
	status = urllib2.urlopen('http://info.vroute.net/vatsim-data.txt')
	#status = open('sample.data')

	SECTION_CLIENTS = False
	SECTION_CLIENTS_MARKER = "!CLIENTS:"

	clients_db = eve_app.data.driver.db['clients']

	data_datetime = datetime.datetime.utcnow()

	for line in status.readlines():
		line = line.strip()

		if SECTION_CLIENTS:
			if line == ';':
				SECTION_CLIENTS = False

				# clear offline clients
				clients_db.remove({ '_updated': { '$lt': data_datetime } })
			else:
				try:
					#
					# CLIENT Capture session
					#
					client_data = assign_client_data(line)
					print line
					clients_raw = line.split(':')
					callsign = clients_raw[0]
					cid = clients_raw[1]
					client_type = clients_raw[3]
					realname = clients_raw[2]
					latitude = clients_raw[5]
					longitude = clients_raw[6]
					altitude = clients_raw[7]
					groundspeed = clients_raw[8]
					heading = clients_raw[38]
					flight_rules = clients_raw[21]
					departure_ICAO = clients_raw[11]
					destination_ICAO = clients_raw[13]
					alternate_ICAO = clients_raw[28]
					requested_flight_level = clients_raw[12]
					requested_speed = clients_raw[10]
					route = clients_raw[30]
					remarks = clients_raw[29]
					aircraft = clients_raw[9]
					updated = clients_db.find_one({ 'callsign': callsign, 'cid': cid, 'client_type': client_type })
					if updated:
						updated['location'] = [ float(longitude), float(latitude) ]
						updated['altitude'] = altitude
						updated['groundspeed'] = groundspeed
						updated['heading'] = heading
						updated['flight_rules'] = flight_rules
						updated['departure_ICAO'] = departure_ICAO
						updated['destination_ICAO'] = destination_ICAO
						updated['alternate_ICAO'] = alternate_ICAO
						updated['requested_flight_level'] = requested_flight_level
						updated['requested_speed'] = requested_speed
						updated['route'] = route
						updated['remarks'] = remarks
						updated['aircraft'] = aircraft
						updated['_updated'] = data_datetime
						clients_db.save(updated)
					else:
						insert = {
							'callsign': callsign,
							'cid': cid,
							'client_type': client_type,
							'realname': realname,
							'location': [ float(longitude), float(latitude) ],
							'altitude': altitude,
							'groundspeed': groundspeed,
							'heading': heading,
							'flight_rules': flight_rules,
							'departure_ICAO': departure_ICAO,
							'destination_ICAO': destination_ICAO,
							'alternate_ICAO': alternate_ICAO,
							'requested_flight_level': requested_flight_level,
							'requested_speed': requested_speed,
							'route': route,
							'remarks': remarks,
							'aircraft': aircraft,
							'_created': data_datetime,
							'_updated': data_datetime
						}
						clients_db.insert_one(insert)
				except Exception as e:
					print e % ' lng:' % clients_raw[6] % ' lat:' % clients_raw[5]
		else:
			if line == SECTION_CLIENTS_MARKER:
				SECTION_CLIENTS = True
	return 'Ok'