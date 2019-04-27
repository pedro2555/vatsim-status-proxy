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
            else:
                _section = f'_split_coords'

            try:
                line = vars(_current_module)[_section](line[1:])
                getattr(self, 'boundaries')[icao].append(line)
            except AttributeError:
                pass

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
        'unknow',
        'unknow1',
        'coords_count',
        'limit1',
        'limit2',
        'name_position')
    return _split_to_dict(keys, line)

def _split_coords(line):
    keys = (
        'lat',
        'lng')
    return _split_to_dict(keys, line)
