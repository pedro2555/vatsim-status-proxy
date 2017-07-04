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
from src import vatsim_data
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

def pre_clients_get_callback(request, lookup):
    # check if newer info can be 
    if vatsim_data.is_data_old_enough(app, 'clients'):
        vatsim_data.pull_vatsim_data(app)
    else:
        print('did not update')

app.on_pre_GET_clients += pre_clients_get_callback

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
