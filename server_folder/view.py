
from flask import Flask, redirect, render_template, Blueprint, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import *
from werkzeug.utils import secure_filename

if __name__ == 'view':
    from model import Runner, Property, Manager, Task, Picture, db, app
else:
    from server_folder.model import Runner, Property, Manager, Task, Picture, db

properties_blueprint = Blueprint('properties', __name__, template_folder = 'templates')

@properties_blueprint.route('/')
def vacant_units():
    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()
    # all_properties = Property.query.all()
    runners = Runner.query.all()

    properties = []
    addresses = {}

    for property in all_properties:
        if property.vacant == True and property.team_id == session['team_id']:
            properties.append(property)

            address = property.address.split(',')

            addresses[property.property_id] = {
                "street": address[0],
                "city": address[1],
                "state": address[2],
                "zipcode": address[3]
            }


            dt = datetime.now()
            date_vacated = property.date_vacated
            days_vacant = (dt - date_vacated).days
            property.days_vacant = days_vacant
            db.session.commit()

    return render_template('properties/vacant_units.html', properties=properties, runners=runners, addresses=addresses)


@properties_blueprint.route('/<property_id>', methods=['POST', 'GET'])
def unit_details(property_id):

    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()
    # all_properties = Property.query.all()
    runners = Runner.query.all()
    property_pics = Picture.query.filter(Picture.property_id == property_id)

    properties = []
    addresses = {}

    for property in all_properties:
        if property.vacant == True and property.team_id == session['team_id']:
            properties.append(property)

            address = property.address.split(',')

            addresses[property.property_id] = {
                "street": address[0],
                "city": address[1],
                "state": address[2],
                "zipcode": address[3]
            }

    if 'manager' in session:
        email = session['manager']
        manager = Manager.query.filter(Manager.email == email).first()
        manager_id = manager.manager_id
        managed_runners = Runner.query.filter(Runner.manager_id == manager_id)
    else:
        email = None
        managed_runners = None

    tasks = Task.query.filter(Task.property_id == property_id).all()

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
        leasing_pics = request.form.getlist('leasing_pics')
        unit_check = request.form.getlist('unit_check')
        picture = request.files['picture']

        if 'manager' in session:
            task = request.form['task']
            occupied = request.form.getlist('occupied')
            runner_id = request.form['runner']


            # Update Runner
            selected_runner = Runner.query.get(runner_id)
            unit.runner_id = selected_runner.runner_id

            # Add Task
            if task:
                new_task = Task(task=f'{task}', completed=False, property_id=property_id)
                db.session.add(new_task)

            # Update Occupied
            if occupied:
                unit.vacant = False
            else:
                unit.vacant = True

        # Update Tasks
        for task in tasks:
            checked_job = request.form.getlist(f'task{task.task_id}')
            if checked_job:
                task.completed = True
            else:
                task.completed = False
                       
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

        # Update Pictures
        if picture:
            from storage import add_to_cloudinary
            filename = secure_filename(picture.filename)
            cover_data = picture.read()
            res = add_to_cloudinary(cover_data, filename)
            if res == 'Error':
                flash('Image name already exists', 'danger')
                return redirect(url_for('homepage'))

            picture = Picture(picture=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", property_id=property_id)
            db.session.add(picture)

        db.session.commit()

        return redirect(url_for('properties.vacant_units'))

    else:

        return render_template('properties/unit_details.html', unit=unit, runner=runner, managed_runners=managed_runners, days_vacant=days_vacant, tasks=tasks, property_pics=property_pics)
