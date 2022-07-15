from flask import Flask, redirect, render_template, Blueprint, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import *

if __name__ == 'view':
    from model import Runner, Property, Manager, db, app
else:
    from server_folder.model import Runner, Property, Manager, db

properties_blueprint = Blueprint('properties', __name__, template_folder = 'templates')

@properties_blueprint.route('/')
def vacant_units():
    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()
    # all_properties = Property.query.all()
    runners = Runner.query.all()

    properties = []


    for property in all_properties:
        if property.vacant == True and property.team_id == session['team_id']:
            properties.append(property)
            dt = datetime.now()
            date_vacated = property.date_vacated
            days_vacant = (dt - date_vacated).days
            property.days_vacant = days_vacant
            db.session

    return render_template('properties/vacant_units.html', properties=properties, runners=runners)


@properties_blueprint.route('/<property_id>', methods=['POST', 'GET'])
def unit_details(property_id):

    if 'manager' in session:
        email = session['manager']
        manager = Manager.query.filter(Manager.email == email).first()
        manager_id = manager.manager_id
        managed_runners = Runner.query.filter(Runner.manager_id == manager_id)
    else:
        email = None
        managed_runners = None

    unit = Property.query.get(property_id)
    runner_id = unit.runner_id
    runner = Runner.query.get(runner_id)

    dt = datetime.now()
    date_vacated = unit.date_vacated
    days_vacant = (dt - date_vacated).days

# IT ONLY LETS ME DO THE STATEMENT ON THE TOP, ANY BELOW FAIL (7/12)
    # if request.method == 'POST' and request.form['runner_set'] == "runner_assigned":
    #     runner_full_name = request.form['runner']
    #     print(runner_full_name)
    #     first, last = runner_full_name.split('_')
    #     selected_runner = Runner.query.filter(Runner.first_name == first and Runner.last_name == last).first()
    #     runner_id = selected_runner.runner_id
    #     unit.runner_id = selected_runner.runner_id
    #     db.session.commit()
    #     return render_template('properties/unit_details.html', unit=unit, runner=selected_runner, managed_runners=managed_runners)
    # elif request.method == 'POST' and request.form['is_occupied'] == 'occupied':
    #     unit.vacant = False
    #     db.session.commit()
    #     return redirect(url_for('properties.vacant_units'))

    if request.method == 'POST':

        if 'manager' in session:
            occupied = request.form.getlist('occupied')

            leasing_pics = request.form.getlist('leasing_pics')
            unit_check = request.form.getlist('unit_check')

            # Update Runner
            runner_id = request.form['runner']
            selected_runner = Runner.query.get(runner_id)
            unit.runner_id = selected_runner.runner_id

            # Update Occupied
            if occupied:
                unit.vacant = False
            else:
                unit.vacant = True

            # Update Unit Check
            if unit_check:
                unit.unit_check_done = True
            else:
                unit.unit_check_done = False

            # Update Leasing Pics
            if leasing_pics:
                unit.leasing_pics_taken = True
            else:
                unit.leasing_pics_taken = False

            db.session.commit()
            return render_template('properties/unit_details.html', unit=unit, runner=selected_runner, managed_runners=managed_runners)

        else:
            leasing_pics = request.form.getlist('leasing_pics')
            unit_check = request.form.getlist('unit_check')

            # Update Unit Check
            if unit_check:
                unit.unit_check_done = True
            else:
                unit.unit_check_done = False

            # Update Leasing Pics
            if leasing_pics:
                unit.leasing_pics_taken = True
            else:
                unit.leasing_pics_taken = False

            db.session.commit()
            return redirect(url_for('properties.vacant_units'))

    else:
        print(unit)
        return render_template('properties/unit_details.html', unit=unit, runner=runner, managed_runners=managed_runners, days_vacant=days_vacant)
