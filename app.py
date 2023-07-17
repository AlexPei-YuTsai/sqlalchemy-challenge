# Import the dependencies
import numpy as np
import datetime as dt

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind = engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    # List all the available routes.
    return(
        """
        <h1><b>Thank you for using the Honolulu Climate API!</b></h1>
        <h3>Below are a list of the available routes:</h3>
        <ul>
          <li>
            /api/v1.0/precipitation
              <ul>
                <li>Retrieves precipitation data from the last 12 recorded months of the database (Includes all stations)</li>
              </ul>
          </li>
          <li>
            /api/v1.0/stations
              <ul>
                <li>Retrieves a list of the climate stations in the database</li>
              </ul>
          </li>
          <li>
            /api/v1.0/tobs
              <ul>
                <li>Retrieves temperature data of the most active climate station from the last 12 recorded months of the database</li>
              </ul>
          </li>
          <li>
            /api/v1.0/(start)
              <ul>
                <li>Retrieves minimum, maximum, and average temperature data from a specified start range</li>
              </ul>
          </li>
          <li>
            /api/v1.0/(start)/(end)
              <ul>
                <li>Retrieves minimum, maximum, and average temperature data from a specified start and end range</li>
              </ul>
          </li>
        </ul>
        Please fill in the (start) and/or (end) fields in the format of <b>YYYY-MM-DD</b>
        """
    )

@app.route("/api/v1.0/precipitation")
def get_prcp():
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value

    # Start SQL session
    session = Session(bind = engine)

    # Retrieve the last 12 months of precipitation data
    # Starting from the most recent data point in the database. The query itself returns a String, so we have to convert that
    for i in session.query(func.max(Measurement.date)).first():
        latest_date = dt.datetime.strptime(i, "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    condition_date = latest_date.replace(year=latest_date.year-1)

    # Call the query
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= condition_date.strftime("%Y-%m-%d")).order_by(Measurement.date)

    # Make sure to close open sessions
    session.close()

    # Organize everything into its proper JSON response
    # date as key, prcp as value
    return jsonify([{date:prcp} for date, prcp in query])

@app.route("/api/v1.0/stations")
def get_stations():
    # Return a JSON list of stations from the dataset

    # Start SQL session
    session = Session(bind = engine)

    # Grab everything Station-related
    query = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)

    # Make sure to close open sessions
    session.close()

    # Organize everything into its proper JSON response
    result_list = []
    for station, name, latitude, longitude, elevation in query:
        result_dict={}
        result_dict["station"]=station
        result_dict["name"]=name
        result_dict["latitude"]=latitude
        result_dict["longitude"]=longitude
        result_dict["elevation"]=elevation
        result_list.append(result_dict)

    # Return the JSON representation of your dictionary
    return jsonify(result_list)

@app.route("/api/v1.0/tobs")
def get_tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data
    session = Session(bind = engine)

    # Find most active station, best_station[0][0] used to access first element of list of tuples
    best_station = [row for row in session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()][0][0]
    
    # Find "previous year"
    # Starting from the most recent data point in the database. The query itself returns a String, so we have to convert that
    for i in session.query(func.max(Measurement.date)).first():
        latest_date = dt.datetime.strptime(i, "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    condition_date = latest_date.replace(year=latest_date.year-1)

    # Call the query
    query = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= condition_date.strftime("%Y-%m-%d")).filter(Measurement.station == best_station).order_by(Measurement.date)

    # Make sure to close open sessions
    session.close()

    # Organize everything into its proper JSON response
    result_list = []
    for station, date, tobs in query:
        result_dict={}
        result_dict["station"]=station
        result_dict["date"]=date
        result_dict["tobs"]=tobs
        result_list.append(result_dict)
    # Return a JSON list of temperature observations for the previous year
    return jsonify(result_list)

@app.route("/api/v1.0/<start>")
def get_temps_1end(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
    session = Session(bind = engine)

    # Some error handling - Returns a special message if the desired search is out of the bounds of the dataset's valid dates
    # date[0] is the last day of the dataset, date[1] is the first
    date = [i for i in session.query(func.max(Measurement.date), func.min(Measurement.date)).first()]
    if (start<date[1]):
        return jsonify({"error": f"Invalid input/Input out of range"}), 404

    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date)

    # Make sure to close open sessions
    session.close()

    # Organize everything into its proper JSON response
    result_list = []
    for TMIN, TMAX, TAVG in query:
        result_dict={}
        result_dict["TMIN"]=TMIN
        result_dict["TMAX"]=TMAX
        result_dict["TAVG"]=TAVG
        result_list.append(result_dict)

    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    return jsonify(result_list)

@app.route("/api/v1.0/<start>/<end>")
def get_temps_2ends(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range
    session = Session(bind = engine)

    # Some error handling - Returns a special message if the desired search is out of the bounds of the dataset's valid dates
    # date[0] is the last day of the dataset, date[1] is the first
    date = [i for i in session.query(func.max(Measurement.date), func.min(Measurement.date)).first()]
    if (start<date[1] or end>date[0]):
        return jsonify({"error": f"Invalid input/Input out of range"}), 404

    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date)

    # Make sure to close open sessions
    session.close()

    # Organize everything into its proper JSON response
    result_list = []
    for TMIN, TMAX, TAVG in query:
        result_dict={}
        result_dict["TMIN"]=TMIN
        result_dict["TMAX"]=TMAX
        result_dict["TAVG"]=TAVG
        result_list.append(result_dict)
    # For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date to the end date, inclusive
    return jsonify(result_list)

if __name__ == "__main__":
    app.run(debug=True)