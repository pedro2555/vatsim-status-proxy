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

_current_module = sys.modules[__name__] # pylint: disable=C0103

# pylint: disable=R0902, R0903
class FirsPolygons():
    """Dataclass holding the information provided by VATSpy.dat file from source."""
    def __init__(self, file):
        self.firs_polygons = list()

        def get_polygons(head, items):
            try:
                line = list()
                for item in items:
                    line = item[:-1]
                    line = vars(_current_module)['_split_polygons_data'](line)
                head = head[:-1]
                head = vars(_current_module)['_split_polygons_head'](head)

                getattr(self, 'firs_polygons').append({'head':head, 'polygon':line})
            except AttributeError:
                pass

        str_to_split = str()

        for item in file:
            if item[1].isalpha():
                str_to_split += '\n{}'.format(item)
            else:
                str_to_split += '\r{}'.format(item)

        data = [x.replace('\nA', 'A').split('\n\\r') for x in str_to_split.split('\n\n')]

        for items in data:
            fir_head = items[0]
            fir_polygon_list = [x for x in items[1:]]
            get_polygons(fir_head, fir_polygon_list)

    @staticmethod
    def from_file(datafile='FIRBoundaries.dat'):
        """Returns a valid FIR's polygons.

        Args:
            datafile (str): A valid FIRBoundaries.dat file from VATSPY software.

        Returns:
            FirsPolygons: list with status file information."""
        with open(datafile, 'r', encoding="ISO-8859-1") as file:
            file = file.readlines()
        return FirsPolygons(file)

def _split_to_list(keys, line, *, separator='|'):
    values = line.split(separator)[:len(keys)]
    assert len(keys) == len(values), f'{len(keys)} != {len(values)} for {line}'
    return {key: value for key, value in zip(keys, values)}

def _split_polygons_head(line):
    keys = (
        'icao')
    return _split_to_list(keys, line)

def _split_polygons_data(line):
    keys = (
        'lat',
        'lng')
    return _split_to_list(keys, line)
