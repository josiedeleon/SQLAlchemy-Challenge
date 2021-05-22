
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

#Inspect
inspector = inspect(engine)

#Flask
app = Flask(__name__)


