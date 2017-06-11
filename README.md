# VATSIM Status Proxy

A RESTfull API for VATSIM status servers.

## Getting Started

The project is currently live at <a href="https://vatsim-status-proxy.herokuapp.com"><img src="https://www-assets3.herokucdn.com/assets/logo-purple-08fb38cebb99e3aac5202df018eb337c5be74d5214768c90a8198c97420e4201.svg" height="15px" /></a>, however if you wish to have a copy in your own enviroment follow the steps in Prerequisites and Installing.

### Prerequisites

Although not a requirement, access to a Linux shell is assumed.

Your environment will require the following components installed and configured:

 * <a href="https://www.python.org/">Python 2.7 <img src="https://www.python.org/static/img/python-logo.png" height="15px" /></a>
 * <a href="https://www.mongodb.com/">MongoDB <img src="https://webassets.mongodb.com/_com_assets/global/mongodb-logo-white.png" height="15px" /></a>

### Installing

Clone the project from GitHub and navigate to that folder

```
git clone https://github.com/pedro2555/vatsim-status-proxy.git
cd vatsim-status-proxy
```

Initialize a Python virtual environment

```
virtualenv .
source bin/activate
```

Install project requirements

```
pip install -r requirements
```

Make sure the database settings in [settings.py](settings.py) match your installation settings.

```
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'vatsim-status-proxy')
```

You should now be able to run the server

```
python run.py
```

## Built With

* <a href="">Python-Eve <img src="http://python-eve.org/_static/eve_leaf.png" height="15px"/></a>

## Contributing

Send a pull request here, and explain the changes

## Authors

* **Pedro Rodrigues** - *Initial work*

## License

This project is licensed under the GNU GPL v2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* VATSIM for providing the data
* Python-Eve for the elegant framework that powers this



# vatsim-status-proxy

## Usage Examples

_Notes_ All coordinates are specified as [long,lat] in decimal degrees

Query a connected client by it's callsign

	/clients?where={"callsign":""}

Query connected clients by their current location, given a center coordinate and a radius (in meters)

	/clients?where={"location":{"$near":{"$geometry":{"type":"Point","coordinates":[-7.9398969,37.0178]},"$maxDistance":250000}}}
