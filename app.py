
import numpy as np 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect 
from flask import Flask, jsonify
import datetime as dt 


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station 
session = Session(engine) 
inspector = inspect(engine)
inspector.get_table_names()
app = Flask(__name__)

# latestDate = (session.query(Measurement.date)
#                 .order_by(Measurement.date.desc())
#                 .first())
# latestDate = list(np.ravel(latestDate))[0]

# latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
# latestYear = int(dt.datetime.strftime(latestDate, '%Y'))
# latestMonth = int(dt.datetime.strftime(latestDate, '%m'))
# latestDay = int(dt.datetime.strftime(latestDate, '%d'))

# yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)
# yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')

@app.route("/")
def home():
    return(f"Surf's Up! Weather API for Hawai'i surf conditions<br/>"
            f"-----------------------------------------------------<br/>"
           f"Available app routes:<br/>"
           f"/api/v1.0/stations --- lists all weather observation stations<br/>"
           f"/api/v1.0/precipitation --- latest year of precipitation values<br/>"
           f"/api/v1.0/tobs --- latest year of temperature data<br/>"
           f"/api/v1.0/temp/startdate/ ---gives temperature data from a given start date<br/>"
           f"/api/v1.0/temp/startdate/enddate --- gives the temperature data for a given range of dates<br/>"
           f"date format is (YYYY-MM-DD)<br/>"
           f"dates available: 2010-01-01 to 2017-08-23")


@app.route("/api/v1.0/stations")
def stations():
    results1 = session.query(Station.station, Station.name).all()
    stationNames = list(np.ravel(results1))
    return jsonify(stationNames)

@app.route("/api/v1.0/precipitation")
def precipitation():
    latestDate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
    latestDate = list(np.ravel(latestDate))[0]

    latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
    latestYear = int(dt.datetime.strftime(latestDate, '%Y'))
    latestMonth = int(dt.datetime.strftime(latestDate, '%m'))
    latestDay = int(dt.datetime.strftime(latestDate, '%d'))
    yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)
    yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')

    results2 = session.query(Measurement.date, Measurement.prcp).all()
    precipValues = {date: prcp for date, prcp in results2}
    return jsonify(precipValues)

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.tobs).filter(Station.station == "USC00519281").all()
    tobsData = list(np.ravel(results3))
    return jsonify(tobsData)

@app.route("/api/v1.0/temp/<startdate>/")
@app.route("/api/v1.0/temp/<startdate>/<enddate>")
def tempDates(startdate=None, enddate=None):
    latestDate = (session.query(Measurement.date)
                 .order_by(Measurement.date.desc()).first())
    latestDate = list(np.ravel(latestDate))[0]
    latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
    if enddate == "":
        tempStats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date.between(startdate, lastestDate)).all()
        tempData = list(np.ravel(tempStats))
        return jsonify(tempData)
    else:
        tempStats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date.between(startdate, enddate)).all()
        tempData = list(np.ravel(tempStats))
        return jsonify(tempData)
if __name__== "__main__":
    app.run(debug = True)
