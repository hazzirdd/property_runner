from model import Manager, Property, Runner, connect_to_db, db
from server import app

def create_manager():
    print('Manager')
    Manager.query.delete()

    manager = Manager(email='test@example.com', password='123', first_name='John', last_name='Doe')
    manager1 = Manager(email='test11111@example.com', password='123', first_name='Bob', last_name='Smith')
    manager2 = Manager(email='test2222@example.com', password='123', first_name='Mike', last_name='Goop')


    db.session.add(manager1)
    db.session.add(manager2)
    db.session.add(manager)

    db.session.commit()


def create_runner():
    print('Runner')
    Runner.query.delete()

    runner1 = Runner(email='test@example.com', password='321', first_name='Billy', last_name='Boarker')

    db.session.add(runner1)
    db.session.commit()

def create_properties():
    print('Properties')
    Property.query.delete()

    property1 = Property(cover="https://rentpath-res.cloudinary.com/w_336,h_280,t_rp,cs_tinysrgb,fl_force_strip,c_fill/e_unsharp_mask:50,q_auto/b2e4302075f517442cd3bcd715cfa3f1", address='212 S 500 E', unit='2A', leasing_pics_taken=False, unit_check_done=False, runner_id=1)

    property2 = Property(cover="https://rentpath-res.cloudinary.com/w_336,h_280,t_rp,cs_tinysrgb,fl_force_strip,c_fill/e_unsharp_mask:50,q_auto/b2e4302075f517442cd3bcd715cfa3f1", address='212 S 500 E', unit='1B', leasing_pics_taken=False, unit_check_done=False, runner_id=1)

    property3 = Property(cover="https://rentpath-res.cloudinary.com/w_336,h_280,t_rp,cs_tinysrgb,fl_force_strip,c_fill/e_unsharp_mask:50,q_auto/b2e4302075f517442cd3bcd715cfa3f1", address='212 S 500 E', unit='3A', leasing_pics_taken=False, unit_check_done=False, runner_id=1)


    db.session.add(property1)
    db.session.add(property2)
    db.session.add(property3)

    db.session.commit()

if __name__ == '__main__':
    connect_to_db(app)

    db.create_all()

    create_manager()
    create_runner()
    create_properties()
