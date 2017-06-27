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
	# get the last update time
	clients_db = app.data.driver.db['clients']
	lastest_client = clients_db.find().sort('_updated', -1).limit(1)

	if clients_db.count() == 0 or (datetime.datetime.utcnow() - lastest_client[0]['_updated'].replace(tzinfo=None)).total_seconds() > 30:
		# get new data from VATSIM
		vatsim_data.get_VATSIM_clients(app)


app.on_pre_GET_clients += pre_clients_get_callback

if __name__ == '__main__':
	Bootstrap(app)
	app.register_blueprint(eve_docs, url_prefix='/docs')

	app.run(host=host, port=port, debug=debug)