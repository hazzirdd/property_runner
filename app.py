
from server_folder import app, db
from server_folder.model import Runner, Manager, Property, Task, Picture, Team

import gmaps
import googlemaps
import smtplib
import requests
import datetime
from flask import Flask, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import secure_filename


@app.route('/')
def homepage():
    properties = Property.query.all()
    day = datetime.datetime.today().weekday()

    if day == 6:
        for property in properties:
            if property.vacant == True:
                property.unit_check_done = False
    db.session.commit()

    if "runner" in session:
        team = Team.query.get(session['team_id'])
        team_id = session['team_id']
        runner_email = session["runner"]

        runner = Runner.query.filter(Runner.email == runner_email).first()
        runner_id = runner.runner_id

        properties = Property.query.filter(Property.runner_id == runner_id, Property.team_id == team_id).all()
        all_tasks = Task.query.all()

        needs_leasing_pics = []
        needs_unit_check = []
        needs_tasks = []

        check_count = 0
        for property in properties:
            if property.unit_check_done == False and property.vacant == True:
                nickname = property.address.split(",")
                needs_unit_check.append(nickname[0])
                check_count += 1
        pic_count = 0
        for property in properties:
            if property.leasing_pics_taken == False and property.vacant == True:
                nickname = property.address.split(",")
                needs_leasing_pics.append(nickname[0])
                pic_count += 1
        task_count = 0
        for property in properties:
            for task in all_tasks:
                if property.property_id == task.property_id and property.vacant == True:
                    nickname = property.address.split(",")
                    if nickname[0] not in needs_tasks:
                        needs_tasks.append(nickname[0])
                        task_count += 1

        return render_template('homepage.html', needs_leasing_pics=needs_leasing_pics, needs_unit_check=needs_unit_check, needs_tasks=needs_tasks, check_count=check_count, pic_count=pic_count, task_count=task_count, team=team, person=runner)

    elif "manager" in session:
        runners = Runner.query.all()
        managers = Manager.query.all()
        team_id = session["team_id"]
        team = Team.query.get(session['team_id'])
        manager_email = session['manager']

        manager = Manager.query.filter(Manager.email == manager_email).first()
        manager_id = manager.manager_id

        properties = Property.query.filter(Property.team_id == team_id).all()
        all_tasks = Task.query.all()

        needs_leasing_pics = []
        needs_unit_check = []
        needs_tasks = []

        check_count = 0
        for property in properties:
            if property.unit_check_done == False and property.vacant == True:
                nickname = property.address.split(",")
                needs_unit_check.append(nickname[0])
                check_count += 1
        pic_count = 0
        for property in properties:
            if property.leasing_pics_taken == False and property.vacant == True:
                nickname = property.address.split(",")
                needs_leasing_pics.append(nickname[0])
                pic_count += 1
        task_count = 0
        for property in properties:
            for task in all_tasks:
                if property.property_id == task.property_id and property.vacant == True and task.completed == False:
                    nickname = property.address.split(",")
                    if nickname[0] not in needs_tasks:
                        needs_tasks.append(nickname[0])
                        task_count += 1


        return render_template('homepage.html', needs_leasing_pics=needs_leasing_pics, needs_unit_check=needs_unit_check, needs_tasks=needs_tasks, check_count=check_count, pic_count=pic_count, task_count=task_count, team=team, person=manager)
    else:
        return redirect(url_for("manager_login"))


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')
    else:
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        company_name = request.form['company_name']

        homebase = request.form['homebase']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        address = f"{homebase}, {city}, {state}, {zipcode}"

        if not first_name:
            flash("Please provide a full name", "danger")
            return redirect(url_for('create_account'))
        elif not last_name:
            flash("Please provide a full name", "danger")
            return redirect(url_for('create_account'))
        elif not email:
            flash("Please provide an email address", "danger")
            return redirect(url_for('create_account'))
        elif not password:
            flash("Please provide a password", "danger")
            return redirect(url_for('create_account'))
        elif not company_name:
            flash("Please provide a company name", "danger")
            return redirect(url_for('create_account'))
        elif not homebase:
            flash("Please provide a company address", "danger")
            return redirect(url_for('create_account'))
        elif not city:
            flash("Please provide a city", "danger")
            return redirect(url_for("create_account"))
        elif not state:
            flash("Please provide a state", "danger")
            return redirect(url_for("create_account"))   
        elif not zipcode:
            flash("Please provide a zipcode", "danger")
            return redirect(url_for("create_account"))     


        managers = Manager.query.all()
        for manager in managers:
            if manager.email == email:
                flash(f"Email is not available", 'danger')
                return redirect(url_for('create_account'))
        
        team = Team(name=company_name, homebase=address)
        db.session.add(team)
        db.session.commit()

        manager = Manager(email=email, password=password, first_name=first_name, last_name=last_name, team_id=team.team_id)
        db.session.add(manager)
        db.session.commit()

        flash(f"Account successfully created", 'success')
        return redirect(url_for('manager_login'))


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
                flash(f"Welcome, {runner.first_name}!", "success")
                return redirect(url_for('homepage'))

    flash("Incorrect login", 'danger')
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
                flash(f"Welcome, {manager.first_name} {manager.last_name}!", 'success')
                return redirect(url_for('homepage'))

    flash("Incorrect login", 'danger')
    return render_template('manager_login.html')      


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "manager" in session:
        manager = session["manager"]
        flash(f"Successfully logged out {manager}", 'success')
        session.pop("manager", None)
        session.pop("team_id", None)
    elif "runner" in session:
        runner = session["runner"]
        flash(f"Successfully logged out {runner}", 'success')
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
                flash(f"Email is not available", 'danger')
                return redirect(url_for('create_runner'))

        manager_email = session['manager']
        current_manager = Manager.query.filter(Manager.email == manager_email).first()
        manager_id = current_manager.manager_id

        runner = Runner(email=email, password=password, first_name=first_name, last_name=last_name, manager_id=manager_id, team_id=session['team_id'])
        db.session.add(runner)
        db.session.commit()

        flash(f"Runner successfully created", 'success')
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
    team_id = session['team_id']
    team = Team.query.get(team_id)

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
        if property.address not in properties and property.team_id == team_id:
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

        # If no runner given, auto assign to runner with least amount of units
        if runner_full_name == 'auto':
            runner_assignments = []
            team_properties = Property.query.filter(Property.team_id == team_id, Property.vacant == True)

            error_handler = []
            for property in team_properties:
                error_handler.append(property)

            if not error_handler:
                flash('Cannot auto assign runner at this time', 'danger')
                return redirect(url_for('add_unit'))

            for property in team_properties:
                runner_assignments.append(property.runner_id)

            def least_common_runner():

                runners = Runner.query.filter(Runner.team_id == team_id)

                runner_assignments.sort()
                n = len(runner_assignments)
                min_count = n + 1
                curr_count = 1
 
                for runner in runners:
                    if runner.runner_id not in runner_assignments:
                        return runner.runner_id

                for i in range(1, n):
                    if (runner_assignments[i] == runner_assignments[i - 1]):
                        curr_count += 1
                    else:
                        if (curr_count < min_count):
                            min_count = curr_count
                            res = runner_assignments[i - 1]
                        curr_count = 1

                if (curr_count < min_count):
                    min_count = curr_count
                    res = runner_assignments[n - 1]
                return res

            runner_id = least_common_runner()
            
            selected_runner = Runner.query.get(runner_id) 
            print("AUTO SELECTED:", selected_runner.first_name)   

        else:
            first, last = runner_full_name.split('_')

            selected_runner = Runner.query.filter(Runner.first_name == first and Runner.last_name == last).first()
            runner_name = selected_runner.first_name
            runner_id = selected_runner.runner_id

        if address and new_address:
            flash('Please enter only one address', 'danger')
            return redirect(url_for('add_unit'))
        elif not address and not new_address:
            flash('Please enter an address', 'danger')
            return redirect(url_for('add_unit'))
        elif not unit:
            flash('Please enter a unit', 'danger')
            return redirect(url_for('add_unit'))
        elif not city:
            flash('Please enter a city', 'danger')
            return redirect(url_for('add_unit'))
        elif not state:
            flash('Please enter a state', 'danger')
            return redirect(url_for('add_unit'))
        elif not zipcode:
            flash('Please enter a unit', 'danger')
            return redirect(url_for('add_unit'))
        elif not cover:
            flash('Please enter a cover image', 'danger')
            return redirect(url_for('add_unit'))

        # ADD IMAGE TO CLOUDINARY
        from storage import add_to_cloudinary
        filename = secure_filename(cover.filename)
        # filename = str(hash(filename_base))
        mimetype = cover.mimetype
        cover_data = cover.read()
        res = add_to_cloudinary(cover_data, filename)
        if res == 'Error':
            flash('Image name already exists', 'danger')
            return redirect(url_for('add_unit'))

        # CALCULATE DISTANCE FROM HOMEBASE
        with open('api.txt') as f:
            api_key = f.readline()
            f.close
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'

            if address:
                r = requests.get(url + "origins=" + team.homebase + "&destinations=" + address + "&key=" + api_key)
            elif new_address:
                new_address_full = f"{new_address}, {city}, {state}, {zipcode}"
                r = requests.get(url + "origins=" + team.homebase + "&destinations=" + new_address_full + "&key=" + api_key)

            miles = r.json()['rows'][0]['elements'][0]['distance']['text']
            x = miles.split(' ')
            comma_distance = x[0]
            split_distance = comma_distance.split(',')
            distance_str = ''.join(split_distance)
            distance = float(distance_str)


        if address:

            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=address, zipcode=zipcode, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, distance=distance, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()
        elif new_address:

            new_address_full = f"{new_address}, {city}, {state}, {zipcode}"

            property = Property(cover=f"https://property-runner.mo.cloudinary.net/property-data/.{filename}", address=new_address_full, zipcode=zipcode, unit=unit, leasing_pics_taken=False, unit_check_done=False, vacant=True, date_vacated=date, days_vacant=0, distance=distance, runner_id=runner_id, team_id=session['team_id'])
            db.session.add(property)
            db.session.commit()

        flash('Unit successfully created', 'success')
        return render_template('properties/add_unit.html', properties=properties, runners=runners)


@app.route('/assigned_units')
def assigned_units():
    all_properties = Property.query.order_by(Property.date_vacated.desc()).all()
    runners = Runner.query.all()
    runner_email = session['runner']
    team_id = session['team_id']
    properties = []
    addresses = {}

    for runner in runners:
        if runner_email == runner.email:
            runner = Runner.query.get(runner.runner_id)
            runner_id = runner.runner_id

    for property in all_properties:
        if property.runner_id == runner_id and property.team_id == team_id and property.vacant == True:
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
    properties = []
    addresses = {}

    sort_by = request.form['sort']

    if sort_by == 'runner':
        all_properties = Property.query.order_by(Property.runner_id)

    elif sort_by == 'address':
        all_properties = Property.query.order_by(Property.address)

    elif sort_by == 'vacant':
        all_properties = Property.query.order_by(Property.date_vacated)

    elif sort_by == 'zipcode':
        all_properties = Property.query.order_by(Property.zipcode)

    elif sort_by == 'distance':
        all_properties = Property.query.order_by(Property.distance)

    else:
        all_properties = Property.query.all()

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


@app.route('/sort_units_assigned', methods=['POST', 'GET'])
def sort_units_assigned():
    runners = Runner.query.all()
    # all_properties = Property.query.all()
    properties = []
    addresses = {}

    sort_by = request.form['sort']

    if sort_by == 'runner':
        all_properties = Property.query.order_by(Property.runner_id)

    elif sort_by == 'address':
        all_properties = Property.query.order_by(Property.address)

    elif sort_by == 'vacant':
        all_properties = Property.query.order_by(Property.date_vacated)

    elif sort_by == 'zipcode':
        all_properties = Property.query.order_by(Property.zipcode)

    elif sort_by == 'distance':
        all_properties = Property.query.order_by(Property.distance)

    else:
        all_properties = Property.query.all()
        
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

    return render_template('assigned_units.html', properties=properties, runners=runners, addresses=addresses)

@app.route('/delete_pic/<picture_id>', methods=['POST'])
def delete_pic(picture_id):
    picture = Picture.query.filter(Picture.picture_id == picture_id).one()

    pic_split = picture.picture.split('/')

    dot_filename = pic_split[-1]

    filename = dot_filename[1:]

    from storage import delete_from_cloudinary
    delete_from_cloudinary(filename)

    db.session.delete(picture)
    db.session.commit()

    return redirect(url_for('properties.vacant_units'))



@app.route('/map')
def map():

    with open('api.txt') as f:
        api_key = f.readline()
        f.close


    map_client = googlemaps.Client(api_key)
    work_place_address = '411 W 7200 S, Midvale, UT'
    home_address = '451 E 8400 S, Sandy, UT'

    home = '45 200 N, American Fork, Ut, 84003'
    work = '1174 Graystone Way, Salt Lake City, UT, 84106'

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'

    r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + api_key)

    miles = r.json()['rows'][0]['elements'][0]['distance']['text']
    time = r.json()['rows'][0]['elements'][0]['duration']['text']

    # seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]

    print("The total travel time from home to work is", time)
    print("Miles:", miles)




    response = map_client.geocode(work_place_address)
    map = response[0]['geometry']

    # from gmplot import gmplot
    # # Create the map plotter:
    # apikey = '' # (your API key here)
    # gmap = gmplot.GoogleMapPlotter(37.766956, -122.448481, 14, api_key=api_key)

    # # Mark a hidden gem:
    # gmap.marker(37.770776, -122.461689, color='cornflowerblue')

    # # Highlight some attractions:
    # attractions_lats, attractions_lngs = zip(*[
    #     (37.769901, -122.498331),
    #     (37.768645, -122.475328),
    #     (37.771478, -122.468677),
    #     (37.769867, -122.466102),
    #     (37.767187, -122.467496),
    #     (37.770104, -122.470436)
    # ])
    # gmap.scatter(attractions_lats, attractions_lngs, color='#3B0B39', size=40, marker=False)

    # # Outline the Golden Gate Park:
    # golden_gate_park = zip(*[
    #     (37.771269, -122.511015),
    #     (37.773495, -122.464830),
    #     (37.774797, -122.454538),
    #     (37.771988, -122.454018),
    #     (37.773646, -122.440979),
    #     (37.772742, -122.440797),
    #     (37.771096, -122.453889),
    #     (37.768669, -122.453518),
    #     (37.766227, -122.460213),
    #     (37.764028, -122.510347)
    # ])
    # gmap.polygon(*golden_gate_park, color='cornflowerblue', edge_width=10)

    # # Draw the map to an HTML file:
    # gmap.draw('map.html')


    return render_template('maps/map.html', map=map)


@app.route('/mymap')
def mymap():

    return render_template('maps/mymap.html')

@app.route('/delete/<property_id>', methods=['POST', 'GET'])
def delete(property_id):

    tasks = Task.query.filter(Task.property_id == property_id)
    if tasks:
        for task in tasks:
            db.session.delete(task)

    property = Property.query.get(property_id)
    pic_split = property.cover.split('/')
    dot_filename = pic_split[-1]
    filename = dot_filename[1:]

    from storage import delete_from_cloudinary
    delete_from_cloudinary(filename)

    db.session.delete(property)
    db.session.commit()
    
    
    print(f'{property_id} DELETED')


    return redirect(url_for('past_units'))


if __name__ == '__main__':
    app.run(debug=True)
