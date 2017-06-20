#!/usr/bin/env python
"""
VATSIM Status Proxy.
Copyright (C) 2017  Pedro Rodrigues <prodrigues1990@gmail.com>

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
def parse_raw_location(latitude, longitude):
	"""Groups decimal latitude and longitude values into a `location` list

    Args:
        latitude (float): Decimal latitude, type float or parseable from string.
        longitude (float): The second parameter, type float or parseable from string.

    Returns:
        list: [`longitude`, `latitude`]
	"""
	# As per GEOJson Spec (RFC 7946) location coordinates are ordered longitude,latitude
	return [ float(longitude), float(latitude) ]