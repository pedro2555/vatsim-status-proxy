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
from eve import Eve
from . import vatsim_data, icao_data

app = Eve(__name__)

def pre_get_callback(resource, request, lookup):
    if resource not in ['clients', 'prefiles', 'servers']:
        return

    if app.debug or vatsim_data.should_update():
        vatsim_data.update()

app.on_pre_GET += pre_get_callback

@app.route('/firs/update', methods=['GET'])
def update_firs():
    icao_data.import_data(
        'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/airspaces/zones/fir-list',
        '2a877ab0-4ed2-11e7-9b2e-d3182793b831')
    return 'Done'