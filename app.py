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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/><br/>"
        f"Example of start and end API call:<br/>"
        f"/api/v1.0/2016-10-02/2016-10-08"
    )

""" Question on REPO asks for dictionary with date as keys, and tobs as value
	This is impossible because there are multiple stations, therefore dates will
	overlap. Dates must be unique in order to make them keys. Also without the station 
	ID, this data does not provide any significant insight. """
@app.route("/api/v1.0/precipitation")
def precipitation():
	""" Return a list of all precipitation values by station ordered by date"""
	results = session.query(measurement.date, measurement.station, measurement.prcp).\
		order_by(measurement.date).all()

	all_prcp = []
	for precip in results:
		prcp_dict = {}
		prcp_dict["date"] = precip.date
		prcp_dict["station"] = precip.station
		prcp_dict["prcp"] = precip.prcp
		all_prcp.append(prcp_dict)

	return jsonify(all_prcp)

""" Returns list of all the stations """
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(measurement.station).\
    	group_by(measurement.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results)) # unravels results into simple list

    return jsonify(all_stations)

""" Returns list of all temperatures for the last year """
@app.route("/api/v1.0/tobs")
def tobs():
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

""" Returns a list of the lowest, average, and highest temp since a specified start date """
@app.route("/api/v1.0/<start>")
def temp_start(start):
	# start should be in format (yyyy-mm-dd)
	results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
		filter(measurement.date >= start).all()

	return jsonify(results)
""" Returns a list of the lowest, average, and highest temp since a specified start and end date """
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
	# start should be in format (yyyy-mm-dd)
	results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
		filter(measurement.date >= start).filter(measurement.date <= end).all()

	return jsonify(results)


if __name__ == '__main__':
	app.run(debug=True)