from server_folder import app, db
from server_folder.model import Runner, Manager, Property

import datetime
from flask import Flask, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import secure_filename



@app.route('/')
def homepage():
    print(f"TEAM ID: {session['team_id']}")
    if "runner" in session:
        return render_template('homepage.html')
    elif "manager" in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for("manager_login"))


@app.route('/runner_login', methods=['POST', 'GET'])
def runner_login():
    if request.method == 'GET':
        return render_template('runner_login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        runners = Runner.query.all()

        for runner in runners:
            if runner.email == email and runner.password == password:
                session["runner"] = email
                session["team_id"] = runner.team_id
                flash(f"Welcome, {email}")
                return redirect(url_for('homepage'))

    flash("Incorrect login")
    return render_template('runner_login.html')      


@app.route('/manager_login', methods=['POST', 'GET'])
def manager_login():
    if request.method == 'GET':
        return render_template('manager_login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        managers = Manager.query.all()

        for manager in managers:
            if manager.email == email and manager.password == password:
                session["manager"] = email
                session["team_id"] = manager.team_id
                flash(f"Welcome, {email} with {session['team_id']} ({manager.team_id})")
                return redirect(url_for('homepage'))

    flash("Incorrect login")
    return render_template('manager_login.html')      


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "manager" in session:
        manager = session["manager"]
        flash(f"Successfully logged out {manager}")
        session.pop("manager", None)
        session.pop("team_id", None)
    elif "runner" in session:
        runner = session["runner"]
        flash(f"Successfully logged out {runner}")
        session.pop("runner", None)
        session.pop("team_id", None)

    return redirect(url_for('manager_login'))


@app.route('/create_runner', methods=['POST', 'GET'])
def create_runner():
    if request.method == 'GET':
        return render_template('create_runner.html')
    else:
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        runners = Runner.query.all()
        for runner in runners:
            if runner.email == email:
                flash(f"Email is not available")
                return redirect(url_for('create_runner'))

        manager_email = session['manager']
        current_manager = Manager.query.filter(Manager.email == manager_email).first()
        manager_id = current_manager.manager_id

        runner = Runner(email=email, password=password, first_name=first_name, last_name=last_name, manager_id=manager_id, team_id=session['team_id'])
        db.session.add(runner)
        db.session.commit()

        flash(f"Runner successfully created")
        return redirect(url_for('homepage'))


@app.route('/past_units', methods=['GET', 'POST'])
def past_units():
    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()

    properties = []

    for property in all_properties:
        if property.vacant == False and property.team_id == session['team_id']:
            properties.append(property)

    return render_template('properties/past_units.html', properties=properties)


@app.route('/past_units/<property_id>', methods=['GET', 'POST'])
def past_unit_details(property_id):
    unit = Property.query.get(property_id)
    runner_id = unit.runner_id
    runner = Runner.query.get(runner_id)

    if request.method == 'POST':
        unit.vacant = True
        db.session.commit()
        return redirect(url_for('past_units'))
    else:
        return render_template('properties/past_unit_details.html', unit=unit, runner=runner)


@app.route('/add_unit', methods=['POST', 'GET'])
def add_unit():
    runners = Runner.query.order_by(Runner.first_name.desc()).all()
    all_properties = Property.query.order_by(Property.address.desc()).all()
    properties = []
    for property in all_properties:
        if property.address not in properties:
            properties.append(property.address)

    if request.method == 'GET':
        return render_template('properties/add_unit.html', properties=properties, runners=runners)

    elif request.method == 'POST':
        address = request.form['address']
        new_address = request.form['new_address'].strip()
        unit = request.form['unit'].strip()
        date = request.form['date']
        runner_full_name = request.form['runner']
        cover = request.files['cover']

        first, last = runner_full_name.split('_')

        selected_runner = Runner.query.filter(Runner.first_name == first and Runner.last_name == last).first()
        runner_name = selected_runner.first_name
        runner_id = selected_runner.runner_id

        if address and new_address:
            flash('Please enter only one address')
            return redirect(url_for('add_unit'))
        elif not address and not new_address:
            flash('Please enter an address')
            return redirect(url_for('add_unit'))
        elif not unit:
            flash('Please enter a unit')
            return redirect(url_for('add_unit'))
        elif not cover:
            flash('Please enter a cover image')
            return redirect(url_for('add_unit'))

        from storage import add_to_cloudinary
        filename = secure_filename(cover.filename)
        mimetype = cover.mimetype
        cover_data = cover.read()
        add_to_cloudinary(cover_data, filename)


        if address:
            print(f"Address: {address} | Unit: {unit} | Vacated On: {date} | Runner: {runner_id}")
            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=address, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()
        elif new_address:
            print(f"New Address: {new_address} | Unit: {unit} | Vacated On: {date} | Runner: {runner_name}")
            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=new_address, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()

        flash('Unit successfully created')
        return render_template('properties/add_unit.html', properties=properties, runners=runners)

if __name__ == '__main__':
    app.run(debug=True)
