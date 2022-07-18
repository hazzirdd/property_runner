# from server_folder.model import Manager, Property, Runner, connect_to_db, db
# from app import app

from model import Team, Manager, Property, Runner, Task, connect_to_db, db

def create_team():
    print('Team')
    Team.query.delete()

    team1 = Team(name='Property Kings')
    team2 = Team(name='Apartment Care Plus')
    team3 = Team(name='Investment Home Advisors')

    db.session.add(team1)
    db.session.add(team2)
    db.session.add(team3)
    db.session.commit()


def create_manager():
    print('Manager')
    Manager.query.delete()

    manager = Manager(email='test@example.com', password='123', first_name='John', last_name='Doe', team_id=2)
    manager1 = Manager(email='test11111@example.com', password='123', first_name='Bob', last_name='Smith', team_id=1)
    manager2 = Manager(email='test2222@example.com', password='123', first_name='Mike', last_name='Goop', team_id=3)

    db.session.add(manager1)
    db.session.add(manager2)
    db.session.add(manager)
    db.session.commit()


def create_runner():
    print('Runner')
    Runner.query.delete()

    runner1 = Runner(email='test@example.com', password='321', first_name='Billy', last_name='Boarker', manager_id=1, team_id=1)
    runner2 = Runner(email='test2@example.com', password='000', first_name='Garrett', last_name='Barry', manager_id=1, team_id=1)

    db.session.add(runner1)
    db.session.add(runner2)
    db.session.commit()


def create_properties():
    print('Properties')
    Property.query.delete()

    property1 = Property(cover="https://property-runner.mo.cloudinary.net/property-data/4-plex.jpg", address='212 S 500 E, Salt Lake City, UT, 84103', zipcode=84013, unit='1A', leasing_pics_taken=False, unit_check_done=False, vacant=True, days_vacant=1, date_vacated='20220707 01:00:00 AM', runner_id=1, team_id=1)

    property2 = Property(cover="https://property-runner.mo.cloudinary.net/property-data/4-plex.jpg", address='212 S 500 E, Salt Lake City, UT, 84103', zipcode=84013, unit='2B', leasing_pics_taken=False, unit_check_done=False, vacant=True, days_vacant=7, date_vacated='20220701 01:00:00 AM', runner_id=1, team_id=1)

    property3 = Property(cover="https://property-runner.mo.cloudinary.net/property-data/4-plex.jpg", address='212 S 500 E, Salt Lake City, UT, 84103', zipcode=84013, unit='3A', leasing_pics_taken=False, unit_check_done=False, vacant=True, days_vacant=5, date_vacated='20220704 01:00:00 AM', runner_id=1, team_id=1)

    property4 = Property(cover="https://property-runner.mo.cloudinary.net/property-data/test.jpg", address='51 N King Drive, Holladay, UT, 84117', zipcode=84117, unit= 'House', leasing_pics_taken=False, unit_check_done=False, vacant=True, days_vacant=0, date_vacated='20220710 01:00:00 AM', runner_id=2, team_id=1)

    property5 = Property(cover="https://property-runner.mo.cloudinary.net/property-data/triplex.jpg", address='3709 S 580 E, South Salt Lake, UT, 84106', zipcode=84106, unit= '1B', leasing_pics_taken=False, unit_check_done=False, vacant=True, days_vacant=0, date_vacated='20220710 01:00:00 AM', runner_id=2, team_id=2)

    db.session.add(property1)
    db.session.add(property2)
    db.session.add(property3)
    db.session.add(property4)
    db.session.add(property5)
    db.session.commit()


def create_task():
    print('Tasks')
    Task.query.delete()

    task1 = Task(task='Remove for least sign from window', completed=False, property_id=1)
    db.session.add(task1)
    db.session.commit()

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)

    db.create_all()

    create_team()
    create_manager()
    create_runner()
    create_properties()
    create_task()