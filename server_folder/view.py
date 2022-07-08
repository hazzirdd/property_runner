from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

from server_folder.model import Runner, Property, Manager

properties_blueprint = Blueprint('properties', __name__, template_folder = 'templates')

@properties_blueprint.route('/')
def vacant_units():
    properties = Property.query.order_by(Property.unit.asc()).all()
    return render_template('properties/vacant_units.html', properties=properties)