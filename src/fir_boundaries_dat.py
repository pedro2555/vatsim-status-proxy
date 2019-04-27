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
from collections import defaultdict
import geojson

_current_module = sys.modules[__name__] # pylint: disable=C0103

# pylint: disable=R0903, R0902
class FIRBoundaries():
    """Dataclass holding the information provided by FIRBoundaries.dat."""
    def __init__(self, lines):
        self.boundaries = defaultdict(list)

        for line in lines:
            line.strip()
            if line[1].isalpha():
                icao = line.split('|')[0]
                _section = f'_split_infos'
                try:
                    line = vars(_current_module)[_section](line)
                    getattr(self, 'boundaries')[icao] = defaultdict(list)
                    getattr(self, 'boundaries')[icao]['infos'] = line
                except AttributeError:
                    pass
            else:
                _section = f'_split_coords'
                try:
                    line = vars(_current_module)[_section](line)
                    getattr(self, 'boundaries')[icao]['boundaries'].append(line)
                except AttributeError:
                    pass

    def get_fir_polygons(self, icao):
        """Returns a valid geojson boundaries.

        Args:
            icao (str): A valid icao.

        Returns:
            get_fir_polygons: object with status file information."""
        self.boundaries[icao]['boundaries'].append(self.boundaries[icao]['boundaries'][0])
        polygons = geojson.Polygon(
            [[[x['lng'], x['lat']] for x in self.boundaries[icao]['boundaries']]])
        return polygons

    @staticmethod
    def from_file(data='FIRBoundaries.dat'):
        """Returns a valid FIRBoundaries.dat information.

        Args:
            data (str): A valid FIRBoundaries.dat file.

        Returns:
            FIRBoundaries: object with status file information."""
        with open(data, 'r') as file:
            return FIRBoundaries(file.readlines())

def _split_to_dict(keys, line, *, separator='|'):
    values = line.split(separator)[:len(keys)]
    assert len(keys) == len(values), f'{len(keys)} != {len(values)} for {line}'
    return {key: value for key, value in zip(keys, values)}

def _split_infos(line):
    keys = (
        'icao',
        'unknow',
        'unknow1',
        'coords_count',
        'limit1_lat',
        'limit1_lng',
        'limit2_lat',
        'limit2_lng',
        'name_position_lat',
        'name_position_lng')
    result = _split_to_dict(keys, line)
    result['limit1'] = geojson.Point((float(result['limit1_lng']), float(result['limit1_lat'])))
    del result['limit1_lng'], result['limit1_lat']

    result['limit2'] = geojson.Point((float(result['limit2_lng']), float(result['limit2_lat'])))
    del result['limit2_lng'], result['limit2_lat']

    result['name_position'] = geojson.Point(
        (float(result['name_position_lng']), float(result['name_position_lat'])))
    del result['name_position_lng'], result['name_position_lat']

    return result

def _split_coords(line):
    keys = (
        'lat',
        'lng')
    result = _split_to_dict(keys, line)
    types = {
        'lat': float,
        'lng': float
    }
    for key, func in types.items():
        value = result[key].strip()

        value = value if value != '' else 0
        result[key] = func(value)
    return result
