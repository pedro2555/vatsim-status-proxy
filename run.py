from eve import Eve
import os
from flask_bootstrap import Bootstrap
from eve_docs import eve_docs
from src import vatsim_data
import datetime

app = Eve()

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
    debug = False
else:
    port = 5000
    host = '0.0.0.0'
    debug = True

def pre_clients_get_callback(request, lookup):
	# check if newer info can be 
	if (datetime.datetime.utcnow() - vatsim_data.last_data_server_timestamp(app)).total_seconds() > 30:
		vatsim_data.get_VATSIM_clients(app)

app.on_pre_GET_clients += pre_clients_get_callback

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=debug)
