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
from urllib.request import urlopen
from datetime import datetime
import re
from copy import copy

SPECS = {
    'clients': {
        'spec_token': '; !CLIENTS section -',
        'open_token': '!CLIENTS:',
        'close_token': ';',
        'spec': None,
        'validate': lambda doc:
                    ('callsign' in doc and
                     'cid' in doc and
                     'clienttype' in doc),
        'find': lambda doc: {'callsign': doc['callsign'],
                             'cid': doc['cid'],
                             'clienttype': doc['clienttype']},
        'settings': {
            'callsign': str,
            'cid': str,
            'realname': str,
            'clienttype': str
        }
    },
    'prefiles': {
        'spec_token': '; !PREFILE section -',
        'open_token': '!PREFILE:',
        'close_token': ';',
        'spec': None,
        'validate': lambda doc:
                    ('callsign' in doc and
                     'cid' in doc),
        'find': lambda doc: {'callsign': doc['callsign'],
                             'cid': doc['cid']},
        'settings': {
            'callsign': str,
            'cid': str,
            'realname': str,
            'clienttype': str,
            'groundspeed': int,
            'altitude': int
        }
    },
    'servers': {
        'spec_token': '; !SERVERS section -',
        'open_token': '!SERVERS:',
        'close_token': ';',
        'spec': None,
        'validate': lambda doc:
                    ('ident' in doc and
                     'hostname_or_IP' in doc),
        'find': lambda doc: {'ident': doc['ident'],
                             'hostname_or_IP': doc['hostname_or_IP']},
        'settings': {
            'location': str
        }
    }
}


def match_spec_token(line, spec_item):
    """

    Args:
        line:       (string) String to try to match

        Returns:    (string) The name of the match document in `SPECS` or None

    """
    if spec_item not in ('spec_token', 'open_token', 'close_token', 'spec'):
        raise ValueError('Unable to find spec_item %s' % spec_item)

    for name, spec in SPECS.items():
        if line.startswith(spec[spec_item]):
            return name
    return None

def parse_updated_datetime(line):
    """Parses the first line from VATSIM whazupp file for the update Datetime.
    """
    regex_sig = r'^; Created at (\d{2})\/(\d{2})\/(\d{4}) '\
                r'(\d{2}):(\d{2}):(\d{2}) UTC by Data Server V\d.\d$'

    match = re.match(regex_sig, line)

    if not match:
        return None

    return datetime(int(match.groups()[2]), # Year
                    int(match.groups()[1]), # Month
                    int(match.groups()[0]), # Day
                    int(match.groups()[3]), # Hour
                    int(match.groups()[4]), # Minute
                    int(match.groups()[5]), # Second
                    0)                      # Microsecond

    return dt

def assign_from_spec(spec, line, settings):
    """Returns a dictionary by iterating colon separated values in both spec and
    line, like dictionary[spec] = line.

    Args:
            spec:       (string) colon separated list of spec headers
            line:       (string) colon separated list of values matching spec
            headers
            settings    (Object) dict containing any special type handling for
            fields

    Returns:        (dict) A dictionary of spec,line colon separated values
    """
    spec_fragments = spec.split(':')
    line_fragments = line.split(':')

    if len(spec_fragments) != len(line_fragments):
        raise ValueError('spec fragments do not match line fragments (%s %s)' % line, spec)

    result = {}
    for spec_fragment, line_fragment in zip(spec_fragments, line_fragments):
        if spec_fragment != '' and line_fragment != '':
            if spec_fragment in settings:
                result[spec_fragment] = settings[spec_fragment](line_fragment)
            elif line_fragment.isdigit():
                result[spec_fragment] = float(line_fragment)
            else:
                result[spec_fragment] = line_fragment

    return result

def convert_latlong_to_geojson(document):
    """Changes any matching lat,long entries into a single GEOJson entry.
    `document` is expected to have none or more keys that matches
    `^(?P<start>.*)lon(?P<end>g|.*)$` and an equivalent latitude defined by
    `$start + lat + $end[1:]`.

    Args:
            document:       (dict) the document to mutate

    Returns:        (dict) the mutated document
    """
    # search for longitude entries
    new_object = copy(document)
    for key, value in document.items():
        match = re.match('^(?P<start>.*)lon(?P<end>g|.*)$', key)
        if not match:
            continue

        # if we have a match, locate corresponding latitude
        #       latitude key should be similiar to longitude
        #       even if matches are empty (ie.: 'longitude') the regex and
        #       concatenation bellow should work ok.
        # disconsider first letter from second match group (this maybe an
        # issue, since it is a blind decision)
        latitude_key = match.groups()[0] + 'lat' + match.groups()[1][1:]
        if latitude_key not in document:
            continue

        # we can already append the new location, and remove redundant entries in result object
        new_object[match.groups()[0] + 'location'] = [
            0.0 if value == "" else float(value),
            0.0 if document[latitude_key] == "" else float(document[latitude_key])
        ]
        del new_object[key]
        del new_object[latitude_key]
        #print(new_object[match.groups()[0] + 'location'])

    return new_object

def save_document(document, document_type, timestamp, settings, eve_app):
    """Creates or updates a given document and document type

    """
    # we need all this info, otherwise is probably a test or admin, not
    # sure (but theres some cases here and there)
    if settings['validate'](document):

        # lookup existing documents
        clients_db = eve_app.data.driver.db[document_type]
        existing = clients_db.find_one(settings['find'](document))

        document['_updated'] = timestamp
        if existing:
            existing.update(document)
            clients_db.save(existing)
        else:
            document['_created'] = timestamp
            clients_db.insert_one(document)

def is_data_old_enough(eve_app):
    """ Checks for aging data on the mongo backend to decide if downloading
    new data from VATSIM is required

    Args:
            eve_app         (Object):   Eve instance
            document_type   (string):   Mongodb collection name we're checking
    """
    eve_db = eve_app.data.driver.db['dataversion']
    data = eve_db.find_one()
    if data:
        return (datetime.utcnow() - eve_db['_updated']).total_seconds > 30
    else:
        return True # no data, yes please

def set_update_time(eve_app, update_time):
    eve_db = eve_app.data.driver.db['dataversion']
    existing = eve_db.find_one()
    data = {}
    data['_updated'] = update_time
    if existing:
        existing.update(data)
        eve_db.save(existing)
    else:
        data['_created'] = update_time
        eve_db.insert_one(data)

def pull_vatsim_data(eve_app):
    """Downloads, parses, and populates backend mongodb with the latest data
    from VATSIM status servers.

    Args:
            eve_app (Object):   Eve instance
    """
    set_update_time(eve_app, datetime.utcnow()) # avoid concurrent updates
    vatsim_data_file = urlopen('http://info.vroute.net/vatsim-data.txt')
    update_time = None
    open_spec = None
    for line in vatsim_data_file:
        line = line.decode('utf-8', 'ignore')
        line = line.strip()

        if update_time is None:
            update_time = parse_updated_datetime(line)
            # actually use the real update time
            if update_time:
                set_update_time(eve_app, update_time)

        if open_spec is None:
            # listen for spec tokens, and append new spec
            open_spec = match_spec_token(line, 'spec_token')
            if open_spec != None:
                # assign the actual spec line found
                SPECS[open_spec]['spec'] = line.replace(SPECS[open_spec]['spec_token'], '').strip()
                # we're not really on a spec so
                open_spec = None
                continue

            # listen for open tokens
            open_spec = match_spec_token(line, 'open_token')
        else:
            # listen for close tokens
            close = match_spec_token(line, 'close_token')
            if close != None:
                # clear offline clients still on database
                eve_app.data.driver.db[open_spec].remove({'_updated': {'$lt': update_time}})
                open_spec = None
                continue

            # or

            # try match with spec
            document = assign_from_spec(
                SPECS[open_spec]['spec'],
                line,
                SPECS[open_spec]['settings'])
            document = convert_latlong_to_geojson(document)

            # push to db
            save_document(document, open_spec, update_time, SPECS[open_spec], eve_app)
