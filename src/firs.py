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

# pylint: disable=R0903, R0902, R1702, R0912
class Firs():
    """Dataclass holding the information provided by VATSpy.dat file from source."""
    def __init__(self, file):
        self.firs = list()
        self.uirs = list()
        self.airports = list()

        for fir in file:
            fir = fir.split('\n')
            section = fir[0]
            if section == '[FIRs]':
                section = section.replace('[', '').replace(']', '').lower()
                for item in fir:
                    if not item.startswith(';') and not item.startswith('[') and item != '':
                        if item.split('|')[2] != '':
                            try:
                                line = item[:-1]
                                line = vars(_current_module)['_split_firs'](line)
                                getattr(self, section).append(line)
                            except AttributeError:
                                pass
            elif section == '[UIRs]':
                section = section.replace('[', '').replace(']', '').lower()
                for item in fir:
                    if not item.startswith(';') and not item.startswith('[') and item != '':
                        try:
                            line = item[:-1]
                            line = vars(_current_module)['_split_uirs'](line)
                            getattr(self, section).append(line)
                        except AttributeError:
                            pass
            elif section == '[Airports]':
                section = section.replace('[', '').replace(']', '').lower()
                for item in fir:
                    if not item.startswith(';') and not item.startswith('[') and item != '':
                        try:
                            line = item[:-1]
                            line = vars(_current_module)['_split_airports'](line)
                            getattr(self, section).append(line)
                        except AttributeError:
                            pass

    @staticmethod
    def from_file(datafile='VATSpy.dat'):
        """Returns a valid FIR's, UIR's and airports informations.

        Args:
            datafile (str): A valid VATSpy.dat file from VATSPY software.

        Returns:
            Firs: object with status file information."""
        with open(datafile, 'r', encoding="ISO-8859-1") as file:
            file = file.read()
        return Firs(file.replace('\n\n\n', '\n\n').split('\n\n'))

def _split_to_list(keys, line, *, separator='|'):
    values = line.split(separator)[:len(keys)]
    assert len(keys) == len(values), f'{len(keys)} != {len(values)} for {line}'
    return {key: value for key, value in zip(keys, values)}

def _split_firs(line):
    keys = (
        'icao',
        'name',
        'prefix_position')
    return _split_to_list(keys, line)

def _split_airports(line):
    keys = (
        'icao',
        'name',
        'lat',
        'lng',
        'tma_prefix_position',
        'fir')
    return _split_to_list(keys, line)

def _split_uirs(line):
    keys = (
        'prefix_position',
        'name',
        'firs')
    return _split_to_list(keys, line)
