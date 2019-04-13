#!/usr/bin/env python
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
import os
import click
import subprocess

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', '-h', default='0.0.0.0', help='The address the web app will listen in.')
@click.option('--port', '-p', default=5000, help='The TCP port to listen to')
@click.option('--debug', '-d', default=False, is_flag=True, help='Set enviroment mode')
def run(host, port, debug):
    """Runs a development web server."""
    if debug:
        from src import app
        app.run(host=host, port=port, debug=debug)
    else:
        bind = '%s:%s' % (host, port)
        subprocess.call(['gunicorn', 'src:app', '--bind', bind, '--log-file=-'])

@cli.command()
def shell():
    """Runs a shell in the app context."""
    subprocess.call(['flask', 'shell'])

@cli.command()
@click.option('--only', help='Run only the specified test.')
def test(only=None):
    """Runs tests."""
    suite = ['coverage', 'run', '--source=src', '-m', 'unittest', '-v']
    if only:
        suite.append(only)
    subprocess.call(suite)
    subprocess.call(['coverage', 'report', '--show-missing'])

if __name__ == '__main__':
    cli()
