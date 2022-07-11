from multiprocessing import managers
import re
from unittest import runner
from server_folder import app
from server_folder.model import Runner, Manager, Property

from flask import Flask, redirect, render_template, request, url_for, session, flash

@app.route('/')
def homepage():
    if "runner" in session:
        return render_template('homepage.html')
    elif "manager" in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        managers = Manager.query.all()
        runners = Runner.query.all()

        for runner in runners:
            if runner.email == email and runner.password == password:
                session["runner"] = email
                flash(f"Welcome, {email}")
                return redirect(url_for('homepage'))

        for manager in managers:
            if manager.email == email and manager.password == password:
                session["manager"] = email
                flash(f"Welcome, {email}")
                return redirect(url_for('homepage'))

    flash("Incorrect login")
    return render_template('login.html')      


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

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
