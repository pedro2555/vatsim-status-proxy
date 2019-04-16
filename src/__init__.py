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
from datetime import datetime, timedelta
from eve import Eve
from . import icao_data
from .vatsim import VatsimStatus

app = Eve(__name__)

def pre_get_callback(resource, request, lookup):
    if resource not in ['voice_servers', 'clients', 'servers', 'prefiles']:
        return

    db = app.data.driver.db['dataversion']
    dataversion = db.find_one()
    now = datetime.utcnow()
    if dataversion:
        _last_update = dataversion['_updated'].replace(tzinfo=None)
    else:
        _last_update = now - timedelta(seconds=60)
    seconds_since_update = (now - _last_update).total_seconds()

    if seconds_since_update < 60 and not app.debug:
        return

    if dataversion:
        dataversion['_updated'] = now
        db.save(dataversion)
    else:
        db.insert_one({'_created': now, '_updated': now})

    status = VatsimStatus.from_url()
    def save(existing, new):
        new['_updated'] = now
        if existing:
            existing.update(new)
            db.save(existing)
        else:
            new['_created'] = now
            db.insert_one(new)

    db = app.data.driver.db['voice_servers']
    for item in status.voice_servers:
        existing = db.find_one({'hostname_or_IP': item['hostname_or_IP']})
        save(existing, item)
    db = app.data.driver.db['clients']
    for item in status.clients:
        existing = db.find_one(
            {'callsign': item['callsign'], 'cid': item['cid'], 'clienttype': item['clienttype']})
        save(existing, item)
    db = app.data.driver.db['servers']
    for item in status.servers:
        existing = db.find_one({'hostname_or_IP': item['hostname_or_IP']})
        save(existing, item)
    db = app.data.driver.db['prefile']
    for item in status.prefile:
        existing = db.find_one({'callsign': item['callsign'], 'cid': item['cid']})
        save(existing, item)

app.on_pre_GET += pre_get_callback

@app.route('/firs/update', methods=['GET'])
def update_firs():
    icao_data.import_data(
        'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/airspaces/zones/fir-list',
        '2a877ab0-4ed2-11e7-9b2e-d3182793b831')
    return 'Done'

@app.route('/wake')
def wake():
    return '', 100