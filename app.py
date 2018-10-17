import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(measurement.station).\
    	group_by(measurement.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results)) # unravels results into simple list

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
	""" Return a list of all temperatures for the last year"""
	# Query all measurements
	sel = [measurement.station, measurement.tobs, measurement.date]
	results = session.query(*sel).\
		filter(measurement.date > dt.datetime(year=2016, month=8, day=23)).\
		order_by(measurement.date).all()

	all_temps = []
	for temp in results:
		temp_dict = {}
		temp_dict["station"] = temp.station
		temp_dict["tobs"] = temp.tobs
		temp_dict["date"] = temp.date
		all_temps.append(temp_dict)

	return jsonify(all_temps)


if __name__ == '__main__':
	app.run(debug=True)