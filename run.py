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

from eve import Eve
import os
from flask_bootstrap import Bootstrap
from eve_docs import eve_docs
import re
import urllib2
import datetime
import pytz
import src.client_data.client_data as client_data

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

def get_VATSIM_clients():
	status = urllib2.urlopen('http://info.vroute.net/vatsim-data.txt')
	#status = open('sample.data')

	SECTION_CLIENTS = False
	SECTION_CLIENTS_MARKER = "!CLIENTS:"

	clients_db = app.data.driver.db['clients']

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

					new = client_data.parse_client_document(line)

					# check for existing client
					existing = clients_db.find_one({
						'callsign':		new['callsign'],
						'cid': 			new['cid'],
						'client_type':	new['client_type'] })

					if existing:

						# update existing client
						existing.update(new)
						existing['_updated'] = data_datetime
						clients_db.save(existing)
					else:
						# insert new client
						clients_db.insert_one(new)

				except Exception as e:
					print('cid:%s Exception:%s' % (line.split(':')[0], e))
		else:
			if line == SECTION_CLIENTS_MARKER:
				SECTION_CLIENTS = True
	return 'Ok'

def pre_clients_get_callback(request, lookup):
	# get the last update time
	clients_db = app.data.driver.db['clients']
	lastest_client = clients_db.find().sort('_updated', -1).limit(1)

	if clients_db.count() == 0 or (datetime.datetime.utcnow() - lastest_client[0]['_updated'].replace(tzinfo=None)).total_seconds() > 30:
		# get new data from VATSIM
		get_VATSIM_clients()


app.on_pre_GET_clients += pre_clients_get_callback

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=debug)