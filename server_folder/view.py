from flask import Flask, redirect, render_template, Blueprint, request, url_for
from flask_sqlalchemy import SQLAlchemy

if __name__ == 'view':
    from model import Runner, Property, Manager, db, app
else:
    from server_folder.model import Runner, Property, Manager, db, app

properties_blueprint = Blueprint('properties', __name__, template_folder = 'templates')

@properties_blueprint.route('/')
def vacant_units():
    # all_properties = Property.query.order_by(Property.days_vacant.desc()).all()
    all_properties = Property.query.all()


    properties = []

    for property in all_properties:
        if property.vacant == True:
            properties.append(property)

    return render_template('properties/vacant_units.html', properties=properties)


@properties_blueprint.route('/<property_id>', methods=['POST', 'GET'])
def unit_details(property_id):
    unit = Property.query.get(property_id)

    if request.method == 'POST':
        unit.vacant = False
        db.session.commit()
        return redirect(url_for('properties.vacant_units'))
    else:
        print(unit)
        return render_template('properties/unit_details.html', unit=unit)
