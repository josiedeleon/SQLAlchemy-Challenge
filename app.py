
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

#Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#References to Tables
measure = Base.classes.measurement
station = Base.classes.station

#Session
session = Session(engine)

#Flask
app = Flask(__name__)

#Home
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation<br/>"
    )

#Stations
@app.route("/api/v1.0/stations")
def stations():
  session  = Session(engine)
  stations = session.query(station.station, station.name).all()
  return jsonify(stations)

#Tobs
@app.route("/api/v1.0/tobs")
def tobs():
	session  = Session(engine)
	stations_active = session.query(measure.station, func.count(measure.station)).group_by(measure.station).order_by(func.count(measure.station).desc()).all()
	station_mostactive = stations_active[0]
	id_mostactive = station_mostactive[0]
	lowtemp = (session.query(measure.tobs)
                      .filter(measure.station == id_mostactive)
                      .order_by(measure.tobs.asc())
                      .first())
	lowtemp = lowtemp[0]
	hightemp = (session.query(measure.tobs)
                       .filter(measure.station == id_mostactive)
                       .order_by(measure.tobs.desc())
                       .first())
	hightemp = hightemp[0]
	avgtemp = session.query(measure.station, func.avg(measure.tobs)).filter(measure.station == id_mostactive).all()
	data = (session.query(measure.date, measure.tobs)
                   .filter(measure.date >dt.date(2016,8,23))
                   .filter(measure.station == id_mostactive)
                   .order_by(measure.date)
                   .all())
#Precipitation
@app.route("/api/v1.0/precipitation")
def precip():

    session = Session(engine)
    recent_date = session.query(func.max(func.strftime("%Y-%m-%d", measure.date))).limit(5).all()
    recent_date = recent_date[0][0] 
 	#precip_data = session.query(func.strftime("%Y-%m-%d", measure.date), measure.prcp).\
        #filter(func.strftime("%Y-%m-%d", measure.date) >= dt.date(2016,8,23)).all()

    return jsonify(stations)

if __name__ == '__main__':
    app.run()
