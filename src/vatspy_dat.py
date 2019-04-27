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

# pylint: disable=R0903, R0902
class VatspyDat():
    """Dataclass holding the information provided by VATspy.dat."""
    def __init__(self, lines):
        self.countries = list()
        self.airports = list()
        self.firs = list()
        self.uirs = list()
        self.idl = list()

        for line in lines:
            line.strip()
            if line.startswith('['):
                section_name = lines[lines.index(line)][1:len(lines[lines.index(line)])-2].lower()
                lines.pop(lines.index(line))

            if line.startswith(';'):
                continue
            _section = f'_split_{section_name}'
            try:
                line = vars(_current_module)[_section](line)
                getattr(self, section_name).append(line)
            except AttributeError:
                pass

    @staticmethod
    def from_file(data='VATSpy.dat'):
        """Returns a valid VATSpy.dat information.

        Args:
            data (str): A valid VATSpy.dat file.

        Returns:
            VatspyDat: object with status file information."""
        with open(data, 'r') as file:
            return VatspyDat(file.readlines())

def _split_to_dict(keys, line, *, separator='|'):
    values = line.split(separator)[:len(keys)]
    assert len(keys) >= len(values), f'{len(keys)} != {len(values)} for {line}'
    return {key: value for key, value in zip(keys, values)}

def _split_countries(line):
    keys = (
        'country',
        'code',
        'atc_prefix')
    return _split_to_dict(keys, line)

def _split_airports(line):
    keys = (
        'ICAO',
        'name',
        'lat',
        'long',
        'atc_short_prefix',
        'FIR',)
    return _split_to_dict(keys, line)

def _split_firs(line):
    keys = (
        'ICAO',
        'name',
        'atc_prefix')
    return _split_to_dict(keys, line)

def _split_uirs(line):
    keys = (
        'ICAO',
        'name',
        'FIRs')
    return _split_to_dict(keys, line)

def _split_idl(line):
    keys = (
        'lat',
        'lng')
    return _split_to_dict(keys, line)
