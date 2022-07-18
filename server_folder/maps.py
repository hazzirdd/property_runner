import gmaps

with open('api.txt') as f:
    api_key = f.readline()
    f.close

gmaps.configure(api_key='Your api key here')

new_york_coordinates = (40.75, -74.00)
gmaps.figure(center=new_york_coordinates, zoom_level=12)

from flask import Flask, redirect, render_template, Blueprint, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import *

if __name__ == 'view':
    from model import Runner, Property, Manager, db, app
else:
    from server_folder.model import Runner, Property, Manager, db

maps_blueprint = Blueprint('maps', __name__, template_folder = 'templates')

@maps_blueprint.route('/')
def map_page():
    return render_template('map.html')