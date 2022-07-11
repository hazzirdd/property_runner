from server_folder import app

from flask import Flask, redirect, render_template, request, url_for, session, flash

@app.route('/')
def homepage():
    if "user" in session:
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

        session["user"] = email
        flash(f"Welcome, {email}")
        return redirect(url_for('homepage'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Logged out {user}")
    session.pop("user", None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
