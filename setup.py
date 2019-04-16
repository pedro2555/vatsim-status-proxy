
"""
VATSIM Status Proxy.
Copyright (C) 2017 - 2019  Pedro Rodrigues <prodrigues1990@gmail.com>
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
from setuptools import setup, find_packages

setup(
	name='VATSIM Status Proxy',
	version='1.0',
	description = 'VATSIM Status Proxy',
	author = 'Pedro Rodrigues',
	author_email = 'prodrigues1990@gmail.com',
	packages = find_packages(),
	install_requires = [],
	test_suite = 'tests',
)