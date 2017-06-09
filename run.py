#!/usr/bin/env python
"""
VATSIM Status Proxy
Copyright (C) 2017  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of VATSIM Status Proxy.

ACARS API is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

ACARS API is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VATSIM Status Proxy.  If not, see <http://www.gnu.org/licenses/>.
"""

from eve import Eve
import os
from flask_bootstrap import Bootstrap
from eve_docs import eve_docs
import re
import urllib2
import datetime

app = Eve()

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
    debug = False
else:
    port = 5000
    host = '0.0.0.0'
    debug = True

@app.route("/status", methods=['GET'])
def get_status():
	status = urllib2.urlopen('http://info.vroute.net/vatsim-data.txt')
	#status = open('sample.data')

	SECTION_CLIENTS = False
	SECTION_CLIENTS_MARKER = "!CLIENTS:"

	clients_db = app.data.driver.db['clients']

	data_datetime = datetime.datetime.now()

	for line in status.readlines():
		line = line.strip()

		if SECTION_CLIENTS:
			if line == ';':
				SECTION_CLIENTS = False

				# clear offline clients
				clients_db.remove({ '_updated': { '$lt': data_datetime } })
			else:
				#
				# CLIENT Capture session
				#
				clients_raw = line.split(':')
				callsign = clients_raw[0]
				cid = clients_raw[1]
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
				updated = clients_db.find_one({ 'callsign': callsign, 'cid': cid })
				if updated:
					updated['latitude'] = latitude
					updated['longitude'] = longitude
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
						'realname': realname,
						'latitude': latitude,
						'longitude': longitude,
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
		else:
			if line == SECTION_CLIENTS_MARKER:
				SECTION_CLIENTS = True
	return 'Ok'

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=debug)