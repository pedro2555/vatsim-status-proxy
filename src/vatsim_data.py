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