# RUN THE APP
# from server_folder import db

# SEED DATABASE
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
db = SQLAlchemy()

class Manager(db.Model):

    __tablename__ = 'managers'

    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"Manager: |{self.manager_id}|{self.first_name}|{self.last_name}|{self.email}|{self.password}"


class Runner(db.Model):

    __tablename__ = 'runners'

    runner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("managers.manager_id"))


class Property(db.Model):

    __tablename__ = 'properties'
    property_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cover = db.Column(db.String(255))
    address = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(64))
    leasing_pics_taken = db.Column(db.Boolean)
    unit_check_done = db.Column(db.Boolean)
    vacant = db.Column(db.Boolean)
    date_vacated = db.Column(db.DateTime)
    days_vacant = db.Column(db.Integer)
    runner_id = db.Column(db.Integer, db.ForeignKey('runners.runner_id'))

    # runner = db.relationship('Runner', backref=db.backref('properties', order_by=property_id))
    

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hayde:haz@localhost/property_runner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # from app import app
    connect_to_db(app)
    print("Connected to DB.")