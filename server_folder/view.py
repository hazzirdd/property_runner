from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

if __name__ == 'view':
    from model import Runner, Property, Model
else:
    from server_folder.model import Runner, Property, Manager

properties_blueprint = Blueprint('properties', __name__, template_folder = 'templates')

@properties_blueprint.route('/')
def vacant_units():
    properties = Property.query.order_by(Property.days_vacant.desc()).all()
    return render_template('properties/vacant_units.html', properties=properties)

@properties_blueprint.route('/<property_id>')
def unit_details(property_id):

    unit = Property.query.get(property_id)


    return render_template('properties/unit_details.html', unit=unit)
