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

import sys
from datetime import datetime
from urllib.request import urlopen

_current_module = sys.modules[__name__] # pylint: disable=C0103

# pylint: disable=R0903, R0902
class VatsimStatus():
    def __init__(self, lines):
        self.version = None
        self.reload = None
        self.update = None
        self.atis_allow_min = None
        self.connected_clients = None
        self.voice_servers = list()
        self.clients = list()
        self.servers = list()
        self.prefile = list()

        section = None
        for line in lines:
            line = line.strip()
            if line.startswith(';') or line == '':
                continue

            if line.startswith('!'):
                section = line[1:-1].lower().replace(' ', '_')
                continue

            if section == 'general':
                key, value = line.split(' = ')
                key = key.lower().replace(' ', '_')
                try:
                    getattr(self, key)
                except AttributeError:
                    continue
                setattr(self, key, value)
                continue
            else:
                _section = f'_split_{section}'
                try:
                    line = line[:-1]
                    line = vars(_current_module)[_section](line)
                    getattr(self, section).append(line)
                except AttributeError:
                    pass

        self.version = int(self.version)
        self.reload = int(self.reload)
        self.update = datetime.strptime(self.update, r'%Y%m%d%H%M%S')
        self.atis_allow_min = int(self.atis_allow_min)
        self.connected_clients = int(self.connected_clients)

    @staticmethod
    def from_url(url='http://info.vroute.net/vatsim-data.txt'):
        file = urlopen(url)
        return VatsimStatus([line.decode('utf-8', 'ignore') for line in file])

def _split_to_dict(keys, line, *, separator=':'):
    values = line.split(separator)
    assert len(keys) == len(values), f'{len(keys)} != {len(values)} for {line}'
    return {key: value for key, value in zip(keys, values)}

def _split_voice_servers(line):
    keys = (
        'hostname_or_IP',
        'location',
        'name',
        'clients_connection_allowed',
        'type_of_voice_server')
    return _split_to_dict(keys, line)

def _split_clients(line):
    keys = (
        'callsign',
        'cid',
        'realname',
        'clienttype',
        'frequency',
        'latitude',
        'longitude',
        'altitude',
        'groundspeed',
        'planned_aircraft',
        'planned_tascruise',
        'planned_depairport',
        'planned_altitude',
        'planned_destairport',
        'server',
        'protrevision',
        'rating',
        'transponder',
        'facilitytype',
        'visualrange',
        'planned_revision',
        'planned_flighttype',
        'planned_deptime',
        'planned_actdeptime',
        'planned_hrsenroute',
        'planned_minenroute',
        'planned_hrsfuel',
        'planned_minfuel',
        'planned_altairport',
        'planned_remarks',
        'planned_route',
        'planned_depairport_lat',
        'planned_depairport_lon',
        'planned_destairport_lat',
        'planned_destairport_lon',
        'atis_message',
        'time_last_atis_received',
        'time_logon',
        'heading',
        'QNH_iHg',
        'QNH_Mb')
    result = _split_to_dict(keys, line)
    types = {
        'latitude': float,
        'longitude': float,
        'planned_depairport_lat': float,
        'planned_depairport_lon': float,
        'planned_destairport_lat': float,
        'planned_destairport_lon': float,
        'altitude': int,
        'groundspeed': int
    }
    for key, func in types.items():
        value = result[key].strip()
        value = value if value != '' else 0
        result[key] = func(value)
    result['location'] = [result['longitude'], result['latitude']]
    del result['longitude'], result['latitude']
    result['planned_depairport_location'] = [
        result['planned_depairport_lon'],
        result['planned_depairport_lat']]
    del result['planned_depairport_lon'], result['planned_depairport_lat']
    result['planned_destairport_location'] = [
        result['planned_destairport_lon'],
        result['planned_destairport_lat']]
    del result['planned_destairport_lon'], result['planned_destairport_lat']

    return result

def _split_servers(line):
    keys = (
        'ident',
        'hostname_or_IP',
        'location',
        'name',
        'clients_connection_allowed')
    return _split_to_dict(keys, line)

def _split_prefile(line):
    keys = (
        'callsign',
        'cid',
        'realname',
        'clienttype',
        'frequency',
        'latitude',
        'longitude',
        'altitude',
        'groundspeed',
        'planned_aircraft',
        'planned_tascruise',
        'planned_depairport',
        'planned_altitude',
        'planned_destairport',
        'server',
        'protrevision',
        'rating',
        'transponder',
        'facilitytype',
        'visualrange',
        'planned_revision',
        'planned_flighttype',
        'planned_deptime',
        'planned_actdeptime',
        'planned_hrsenroute',
        'planned_minenroute',
        'planned_hrsfuel',
        'planned_minfuel',
        'planned_altairport',
        'planned_remarks',
        'planned_route',
        'planned_depairport_lat',
        'planned_depairport_lon',
        'planned_destairport_lat',
        'planned_destairport_lon',
        'atis_message',
        'time_last_atis_received',
        'time_logon',
        'heading',
        'QNH_iHg',
        'QNH_Mb')
    return _split_to_dict(keys, line)
