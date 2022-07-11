from server_folder import app, db
from server_folder.model import Runner, Manager, Property

from flask import Flask, redirect, render_template, request, url_for, session, flash


@app.route('/')
def homepage():
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
                flash(f"Welcome, {email}")
                return redirect(url_for('homepage'))

    flash("Incorrect login")
    return render_template('manager_login.html')      


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "manager" in session:
        manager = session["manager"]
        flash(f"Successfully logged out {manager}")
        session.pop("manager", None)
    elif "runner" in session:
        runner = session["runner"]
        flash(f"Successfully logged out {runner}")
        session.pop("runner", None)

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

        runner = Runner(email=email, password=password, first_name=first_name, last_name=last_name, manager_id=manager_id)
        db.session.add(runner)
        db.session.commit()

        flash(f"Runner successfully created")
        return redirect(url_for('homepage'))


@app.route('/past_units', methods=['GET', 'POST'])
def past_units():
    all_properties = Property.query.order_by(Property.days_vacant.desc()).all()

    properties = []

    for property in all_properties:
        if property.vacant == False:
            properties.append(property)

    return render_template('properties/past_units.html', properties=properties)


@app.route('/past_units/<property_id>', methods=['GET', 'POST'])
def past_unit_details(property_id):
    unit = Property.query.get(property_id)

    if request.method == 'POST':
        print('POST')
        print(unit)
        unit.vacant = True
        db.session.commit()
        print(unit)
        return redirect(url_for('past_units'))
    else:
        print('GET')
        return render_template('properties/past_unit_details.html', unit=unit)


if __name__ == '__main__':
    app.run(debug=True)
