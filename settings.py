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

import os

firs_schema = {
	'icao': {
		'type': 'string'
	},
	'name': {'type': 'string'},
	'location': {'type': 'Point'},
	'boundaries': {'type': 'Polygon'},
	'callsigns': {
		'type': 'list',
        'schema': {'type': 'string'}
	},
	'sectors': {
		'type': 'list',
        'schema': {
            'name': {'type': 'string'},
			'location': {'type': 'Point'},
            'boundaries': {'type': 'Polygon'},
        	'callsigns': {
        		'type': 'list',
                'schema': {'type': 'string'}
        	}
        }
	}
}
firs = {
	'schema': firs_schema,
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False
}

clients_schema = {
	'callsign': {
		'type': 'string'
	},
	'cid': {
		'type': 'string'
	},
	'realname': {
		'type': 'string'
	},
	'clienttype': {
		'type': 'string'
	},
	'location': {
		'type': 'point'
	},
	'groundspeed': {
		'type': 'number'
	},
	'altitude': {
		'type': 'number'
	}
}
clients = {
	'schema': clients_schema,
	'allow_unknown': True,
	'resource_methods': ['GET'],
	'item_methods': ['GET'],
	'pagination': False,
	'mongo_indexes': {
		'location_2d': [ ('location', '2d') ],
		'location_2dsphere': [ ('location', '2dsphere') ]
	}
}

DOMAIN = {
	'clients': clients,
	'firs': firs
}

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'vatsim-status-proxy')

X_DOMAINS = '*'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
MONGO_QUERY_BLACKLIST = ['$where', '$regex']
