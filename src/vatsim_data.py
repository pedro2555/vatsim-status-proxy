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
from urllib.request import urlopen
import datetime
import pytz
import re
import collections
from copy import copy

specs = {
	'clients': {
		'spec_token': '; !CLIENTS section -',
		'open_token': '!CLIENTS:',
		'close_token': ';',
		'spec': None
	}
}

def match_spec_token(line, spec_item):
	"""

	Args:
		line:	(string) String to try to match

	Returns:	(string) The name of the match document in `specs` or None

	"""
	if spec_item not in ('spec_token', 'open_token', 'close_token', 'spec'):
		raise ValueError('Unable to find spec_item %s' % spec_item)

	for name, spec in specs.items():
		if line.startswith(spec[spec_item]):
			return name
	return None

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
		if spec_fragment != '' and line_fragment != '':
			result[spec_fragment] = line_fragment

	return result

def convert_latlong_to_geojson(document):
	"""Changes any matching lat,long entries into a single GEOJson entry.
	`document` is expected to have none or more keys that matches `^(?P<start>.*)lon(?P<end>g|.*)$` and
	an equivalent latitude defined by `$start + lat + $end[1:]`.

	Args:
		document:	(dict) the document to mutate

	Returns:	(dict) the mutated document
	"""
	# search for longitude entries
	new_object = copy(document)
	for key, value in document.items():
		match = re.match('^(?P<start>.*)lon(?P<end>g|.*)$', key)
		if not match:
			continue

		# if we have a match, locate corresponding latitude
		# 	latitude key should be similiar to longitude
		#	even if matches are empty (ie.: 'longitude') the regex and concatenation bellow should
		#	work ok.
		# disconsider first letter from second match group (this maybe an issue, since it is a blind
		# decision)
		latitude_key = match.groups()[0] + 'lat' + match.groups()[1][1:]
		if latitude_key not in document:
			continue

		# we can already append the new location, and remove redundant entries in result object
		new_object[match.groups()[0] + 'location'] = [
			0.0 if value == "" else float(value),
			0.0 if document[latitude_key] == "" else float(document[latitude_key])
		]
		del new_object[key]
		del new_object[latitude_key]
		#print(new_object[match.groups()[0] + 'location'])

	return new_object

def save_document(document, document_type, timestamp, eve_app):
	"""Creates or updates a given document and document type

	"""
	try:
		# we need all this info, otherwise is probably a test or admin, not sure (but theres some cases here and there)
		if 'callsign' in document and 'cid' in document and 'realname' in document and 'clienttype' in document:
			db = eve_app.data.driver.db[document_type]

			existing = db.find_one({ 'callsign':	document['callsign'],
									 'cid':			document['cid'],
									 'clienttype':	document['clienttype'] })

			document['_updated'] = timestamp
			if existing:
				existing.update(document)
				db.save(existing)
			else:
				document['_created'] = timestamp
				db.insert_one(document)

	except Exception as error:
		raise ValueError('Unable to save document from line %s' % document) from error

def is_data_old_enough(eve_app, document_type):
	try:
		db = eve_app.data.driver.db[document_type]

		# no data, yes please
		if db.count() < 1:
			return True

		# data more than 30 seconds old should be updated
		utc_now = datetime.datetime.utcnow()
		utc_last_update = db.find().sort('_updated', -1).limit(1)[0]['_updated'].replace(tzinfo=None)
		if (utc_now - utc_last_update).total_seconds() > 30:
			return True

		# no positive match, so no
		return False
	except Exception as error:
		print(error)
		return False

def pull_vatsim_data(eve_app):
	vatsim_data_file = urlopen('http://info.vroute.net/vatsim-data.txt')
	update_time = datetime.datetime.utcnow()
	open_spec = None
	for line in vatsim_data_file:
		line = line.decode('utf-8', 'ignore')
		line = line.strip()

		if open_spec == None:
			# listen for spec tokens, and append new spec
			open_spec = match_spec_token(line, 'spec_token')
			if open_spec != None:
				# assign the actual spec line found
				specs[open_spec]['spec'] = line.replace(specs[open_spec]['spec_token'], '').strip()
				# we're not really on a spec so
				open_spec = None
				continue

			# listen for open tokens
			open_spec = match_spec_token(line, 'open_token')
		else:
			# listen for close tokens
			close = match_spec_token(line, 'close_token')
			if close != None:
				# clear offline clients still on database
				eve_app.data.driver.db[open_spec].remove({ '_updated': { '$lt': update_time } })
				open_spec = None
				continue

			# or

			# try match with spec
			try:
				document = assign_from_spec(specs[open_spec]['spec'], line)
			except Exception as error:
				print('Failed to match spec on line %s' % line)
				
			document = convert_latlong_to_geojson(document)

			# push to db
			try:
				save_document(document, open_spec, update_time, eve_app)
			except Exception as error:
				print(error)

def last_data_server_timestamp(eve_app):
	clients = eve_app.data.driver.db['clients']

	if clients.count() < 1:
		return None

	# get the most outdated client stamp
	# (also remove any timezone information, we'll deal with UTC time only)
	return clients.find().sort('_updated', -1).limit(1)[0]['_updated'].replace(tzinfo=None)

def get_VATSIM_clients(eve_app):
	{
		'clients': {
			'spec_token': '; !CLIENTS section -',
			'open_token': '!CLIENTS:',
			'close_token': ';'
		}
	}



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
					client_data = test_assign_from_spec(line)
					client_data = assign_client_data(line)
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
					print(e % ' lng:' % clients_raw[6] % ' lat:' % clients_raw[5])
		else:
			if line == SECTION_CLIENTS_MARKER:
				SECTION_CLIENTS = True
	return 'Ok'