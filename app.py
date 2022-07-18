from server_folder import app, db
from server_folder.model import Runner, Manager, Property

import datetime
from flask import Flask, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import secure_filename



@app.route('/')
def homepage():
    properties = Property.query.all()
    day = datetime.datetime.today().weekday()

    if day == 6:
        for property in properties:
            print(property.address)
            property.unit_check_done = False
    db.session.commit()

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

    if request.method == 'GET':
        for property in all_properties:
            if property.vacant == False and property.team_id == session['team_id']:
                properties.append(property)

        return render_template('properties/past_units.html', properties=properties)

    elif request.method == 'POST':
        runners = Runner.query.all()

        sort_by = request.form['sort']

        if sort_by == 'runner':
            all_properties = Property.query.order_by(Property.runner_id)

        if sort_by == 'address':
            all_properties = Property.query.order_by(Property.address)

        if sort_by == 'vacant':
            all_properties = Property.query.order_by(Property.date_vacated)
            
        for property in all_properties:
            if property.vacant == False and property.team_id == session['team_id']:
                properties.append(property)

        return render_template('properties/past_units.html', properties=properties, runners=runners)


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

    if 'manager' in session:
        email = session['manager']
        manager = Manager.query.filter(Manager.email == email).first()
        manager_id = manager.manager_id
        managed_runners = Runner.query.filter(Runner.manager_id == manager_id)
    else:
        email = None
        managed_runners = None

    all_properties = Property.query.order_by(Property.address.desc()).all()
    properties = []
    for property in all_properties:
        if property.address not in properties:
            properties.append(property.address)

    if request.method == 'GET':
        return render_template('properties/add_unit.html', properties=properties, runners=managed_runners)

    elif request.method == 'POST':
        address = request.form['address']
        new_address = request.form['new_address'].strip().title()
        unit = request.form['unit'].strip().title()
        city = request.form['city'].strip().title()
        state = request.form['state'].strip().title()
        zipcode = request.form['zipcode'].strip()
        date = request.form['date']
        cover = request.files['cover']
        runner_full_name = request.form['runner']

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
        elif not city:
            flash('Please enter a city')
            return redirect(url_for('add_unit'))
        elif not state:
            flash('Please enter a state')
            return redirect(url_for('add_unit'))
        elif not zipcode:
            flash('Please enter a unit')
            return redirect(url_for('add_unit'))
        elif not cover:
            flash('Please enter a cover image')
            return redirect(url_for('add_unit'))

        from storage import add_to_cloudinary
        filename = secure_filename(cover.filename)
        mimetype = cover.mimetype
        cover_data = cover.read()
        res = add_to_cloudinary(cover_data, filename)
        if res == 'Error':
            flash('Image name already exists')
            return redirect(url_for('add_unit'))

        if address:
            print(f"Address: {address} | Unit: {unit} | Vacated On: {date} | Runner: {runner_id}")
            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=address, zipcode=zipcode, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()
        elif new_address:

            new_address_full = f"{new_address}, {city}, {state}, {zipcode}"

            print(f"New Address: {new_address_full} | Unit: {unit} | Vacated On: {date} | Runner: {runner_name}")
            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=new_address_full, zipcode=zipcode, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()

        flash('Unit successfully created')
        return render_template('properties/add_unit.html', properties=properties, runners=runners)


@app.route('/assigned_units')
def assigned_units():
    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()
    runners = Runner.query.all()
    runner_email = session['runner']
    properties = []
    addresses = {}

    for runner in runners:
        if runner_email == runner.email:
            runner = Runner.query.get(runner.runner_id)
            runner_id = runner.runner_id

    for property in all_properties:
        if property.runner_id == runner_id:
            properties.append(property)

            address = property.address.split(',')

            addresses[property.property_id] = {
                "street": address[0],
                "city": address[1],
                "state": address[2],
                "zipcode": address[3]
            }

    session["previous_page"] = "assigned_units"
    return render_template('assigned_units.html', properties=properties, runners=runners, addresses=addresses)

    
@app.route('/sort_units', methods=['POST', 'GET'])
def sort_units():
    runners = Runner.query.all()
    # all_properties = Property.query.all()
    properties = []
    addresses = {}

    sort_by = request.form['sort']

    if sort_by == 'runner':
        all_properties = Property.query.order_by(Property.runner_id)

    if sort_by == 'address':
        all_properties = Property.query.order_by(Property.address)

    if sort_by == 'vacant':
        all_properties = Property.query.order_by(Property.date_vacated)

    if sort_by == 'zipcode':
        all_properties = Property.query.order_by(Property.zipcode)
        
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

    return render_template('properties/vacant_units.html', properties=properties, runners=runners, addresses=addresses)


@app.route('/map')
def map():
    import gmaps
    import googlemaps

    with open('api.txt') as f:
        api_key = f.readline()
        f.close

    # gmaps.configure(api_key=api_key)

    # new_york_coordinates = (40.75, -74.00)
    # Durango = (37.2753,-107.880067)

    # fig = gmaps.figure()
    # layer = gmaps.directions.Directions(Durango, new_york_coordinates, mode='car')

    # fig.add_layer(layer)
    # fig

    map_client = googlemaps.Client(api_key)
    
    work_place_address = '451 E 8400 S'
    map_geocode = map_client.geocode(work_place_address)
    map = map_geocode[0]['geometry'] 


    return render_template('maps/map.html', map=map)


if __name__ == '__main__':
    app.run(debug=True)
