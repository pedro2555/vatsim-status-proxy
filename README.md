# VATSIM Status Proxy [![Build Status](https://travis-ci.org/pedro2555/vatsim-status-proxy.svg?branch=master)](https://travis-ci.org/pedro2555/vatsim-status-proxy)

## Getting Started

More of a cache than a proxy, this  software caches VATSIM status data on-demand. Data is parsed and stored on a MongoDB database, and publicly exposed via a REST api powered by Python-Eve.

The big advantage provided simply lies in the fact we parse the data, and expose database to you. That means you can pull the data that interests you and greatly reduce network fetch times. All fields provided by VATSIM are exposed (currently only the clients section is available) so any query you can think of with those fields will work.

Client location information given as coordinates is actually saved as a GEOJson object. And field the `location` is indexed. That means location based queries are also possible. See examples below.

_To avoid unecessary load on our side and on VATSIM servers, data is cached for a minimum of 30 seconds, and is updated on-demand whenever a client request would result in data more than 30 seconds old. Unfortunatly, since Heroku dynos tend to sleep a lot, and requesting and parsing VATSIM data may take some seconds, the first query may take a bit long to be anwsered._

## How to use

The project is currently live at <a href="https://vatsim-status-proxy.herokuapp.com"><img src="https://www-assets3.herokucdn.com/assets/logo-purple-08fb38cebb99e3aac5202df018eb337c5be74d5214768c90a8198c97420e4201.svg" height="15px" /></a>. For sake of readability, `/` refers to full url of the live version of the project.

### Basic usage

Although not very useful, querying the clients endpoint root, returns a list of all connected clients.
It is still a more streamlined response, so you should be able to use a library of choice to read the data.

```http
GET /clients

200 OK
{  
   "_items":[  
      {  
         "callsign":"N401EL",
         "clienttype":"PILOT",
         "location":[  
            -86.68227,
            34.61644
         ],
         "planned_depairport_location":[  
            0.0,
            0.0
         ],
         "planned_destairport_location":[  
            0.0,
            0.0
         ]
      },
      
      ...
```


You can also query by any single field.

```http
GET /clients?where={"callsign":"N401EL"}

200 OK
{  
   "_items":[  
      {  
         "callsign":"N401EL",
         "clienttype":"PILOT",
         "location":[  
            -86.68227,
            34.61644
         ],
         "planned_depairport_location":[  
            0.0,
            0.0
         ],
         "planned_destairport_location":[  
            0.0,
            0.0
         ]
      }
   ]
}
```

Perhaps more useful, since location field is GEOJson and indexed, you query for clients near a specfic location.

```http
/clients?where={"location":{"$near":{"$geometry":{"type":"Point","coordinates":[long,lat]},"$maxDistance":range}}}

200 OK
{  
   "_items":[  
      {  
         "callsign":"N401EL",
         "clienttype":"PILOT",
         "location":[  
            -86.68227,
            34.61644
         ],
         "planned_depairport_location":[  
            0.0,
            0.0
         ],
         "planned_destairport_location":[  
            0.0,
            0.0
         ]
      },
      
      ...
```

For more query examples you can give a read at the [filtering section on Python-Eve's website](http://python-eve.org/features.html#filtering).

### Prerequisites

_Although not a requirement, access to a Bash unix shell is assumed. Actual development is done on [Bash on Ubuntu for Windows](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide) on Windows 10 machine._

Your environment will require the following components installed and configured:

 * <a href="https://www.python.org/">Python 3 <img src="https://www.python.org/static/img/python-logo.png" height="15px" /></a>
 * <a href="https://www.mongodb.com/">MongoDB <img src="https://webassets.mongodb.com/_com_assets/global/mongodb-logo-white.png" height="15px" /></a>

### Installing

Clone the project from GitHub and navigate to that folder

```bash
git clone https://github.com/pedro2555/vatsim-status-proxy.git
cd vatsim-status-proxy
```

Initialize a Python virtual environment

```bash
virtualenv .
source bin/activate
```

Install project requirements

```bash
pip install -r requirements
```

Make sure the database settings in [settings.py](settings.py) match your installation settings.

```python
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'vatsim-status-proxy')
```

You should now be able to run the server

```bash
python run.py
```

## Built With

* <a href="http://python-eve.org/">Python-Eve <img src="http://python-eve.org/_static/eve_leaf.png" height="15px"/></a>

## Contributing

There are some stuff still on the TODO list (may put that on the issues page), you're free to add any of the following or any other:

* Add PREFILE section parser configuration
* Keep historic data for online clients (may explore the `allow_unkown` options on MongoDB to conserve disk space, not sure how to work it out)
* Plot expected client location during the 30 second update cool down from VATSIM
* Lint and make code more pythonic and/or faster

For development you will need some additional python packages, run the following `pip` command from the project diretory

```bash
pip install -r dev-requirements.txt
```

All code should have appropriate test cases and pass Travis-CI integration. To run the tests on your side run the following `setuputils` command from the project directory

```bash
python setup.py test
```

## Authors

* **Pedro Rodrigues** - *Initial work*

## License

This project is licensed under the GNU GPL v2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* <a href="https://www.vatsim.net/">VATSIM <img src="https://www.vatsim.net/sites/default/files/vatsim_0.png" height="15px"/></a> for providing the data
* <a href="http://python-eve.org/">Python-Eve <img src="http://python-eve.org/_static/eve_leaf.png" height="15px"/></a> for the elegant framework that powers this
