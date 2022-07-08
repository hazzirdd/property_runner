from flask import Flask, render_template
from sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'test'
# Setup DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Migrate(app,db)


@app.route('/')
def welcome():
    return render_template('homepage.html')


@app.route('vacant_units.html')
def vacant_units():

    return render_template('vacant_units.html')



if __name__ == '__main__':
    app.run(debug=True)
