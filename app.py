import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy import inspect 
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
measurement = Base.classes.measurement
inspector = inspect(engine)
for table_name in inspector.get_table_names():
   for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])
print("-----------------------------------")
station = Base.classes.station
inspector = inspect(engine)
for table_name in inspector.get_table_names():
   for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])
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
def welcome_message():
    return(f"Welcome!<br/>"
    f"Thank you for visiting...")

@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).all()
    dictionary = {date:prcp for date, prcp in precipitation}
    return jsonify(dictionary)
    
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    results = list(stations)
    return jsonify(results)
    
@app.route("/api/v1.0/tobs")  
def tobs(): 
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
    results =list(tobs)
    return jsonify(results)

@app.route("/api/v1.0/start")
def start():
    start_date = dt.date(2016, 8, 23) 
    start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()
    start_list = []
    for min, avg, max in start:
        diction = {}
        diction["TMIN"] = min
        diction["TAVG"] = avg
        diction["TMAX"] = max
        start_list.append(diction)   
    return jsonify(start_list)

@app.route("/api/v1.0/start/end")
def start_end():
    start = dt.date(2016, 8, 23) 
    end = dt.date(2017, 8, 23) 
    start_end = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).filter(measurement.date <= end).all()
    start_end_list = []
    for min, avg, max in start_end:
        diction = {}
        diction["TMIN"] = min
        diction["TAVG"] = avg
        diction["TMAX"] = max
        start_end_list.append(diction)   
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)

