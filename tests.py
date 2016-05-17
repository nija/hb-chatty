'''Tests for chatty'''
import unittest

from server import app
from model import *

class ChatModelTests(unittest.TestCase):
    '''Tests for the data model and ORM'''

    def setUp(self):
        pass
    def tearDown(self):
        pass


class ChatAPITests(unittest.TestCase):
    '''Tests for the API routes'''

    def setUp(self):
        pass
    def tearDown(self):
        pass


class ChatWebTests(unittest.TestCase):
    """Tests for the routes"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        '''Checking the root route'''
        result = self.client.get("/")
        self.assertIn("Please chat with me", result.data)
        self.assertEqual(result.status_code, 200)

    # def test_rsvp(self):
    #     '''Checking... post something something'''
    #     result = self.client.post("/process_msg_event",
    #                               data={'name': "Jane", 'data': "jane@jane.com"},
    #                               follow_redirects=True)

    #     self.assertIn("jane@jane", result.data)
    #     self.assertEqual(result.status_code, 200)
        #self.assertNotIn("Please RSVP", result.data)


# def test_seed_once(app, db_uri):
#    '''Create example data for the test database.'''
#     connect_to_db(app, db_uri)

#     # Get to a known good state
#     seed_once(app)

#     # Get users
#     balloonicorn = db.session.query(User).get(1)

# def test_create_get_users(app):
#     '''Create and insert Users'''
#     balloonicorn = db.session.query(User).get(1)
#     # balloonicorn = User(name="Balloonicorn")
#     grace = User(name="Grace Hopper")
#     # db.session.add(balloonicorn)
#     db.session.add(grace)
#     db.session.commit()

# def test_get_users(app):
#     users = User.query.all()
#     print users

# def test_join_room(app):
#     fran = User(name='Fran Allen')
#     db.session.add(fran)
#     db.session.commit()
#     main_room = db.session.query(Room).get(1)
#     fran = User.query.filter(User.name == 'Fran Allen').first()
#     db.session.add(main_room.join_room(fran))
#     # db.session.add(main_room.join_room(balloonicorn))
#     db.session.commit()
#     print main_room.users
#     #FIXME:
#     # assert fran in users

# def test_get_rooms(app):
#     ''' '''
#     rooms = Room.query.all()
#     room_users = RoomUser.query.all()
#     print rooms
#     print room_users

# def test_create_get_messages(app):

#     balloonicorn = db.session.query(User).get(1)
#     grace = User.query.filter(User.name == 'Grace Hopper').first()
#     main_room = db.session.query(Room).get(1)
#     import pdb; pdb.set_trace()
#     a_message = Message(room=main_room, user=grace, data="Please cut off a nanosecond and send it over to me")
#     b_message = Message(room=main_room, user=grace, data='I need something to compare this to. Could I please have a microsecond?')
#     c_message = Message(room=main_room, user=grace, data='I had a running compiler and nobody would touch it... they carefully told me, computers could only do arithmetic; they could not do programs.')
#     d_message = Message(room=main_room, user=grace, data="I've always been more interested in the future than in the past.")
#     e_message = Message(room=main_room, user=grace, data='Life was simple before World War II. After that, we had systems.')
#     f_message = Message(room=main_room, user=grace, data='A ship in port is safe; but that is not what ships are built for. Sail out to sea and do new things.')
#     g_message = Message(room=main_room, user=grace, data='The wonderful thing about standards is that there are so many of them to choose from.')
#     h_message = Message(room=main_room, user=grace, data="In pioneer days they used oxen for heavy pulling, and when one ox couldn't budge a log, they didn't try to grow a larger ox. We shouldn't be trying for bigger computers, but for more systems of computers.")
#     i_message = Message(room=main_room, user=grace, data="It's easier to ask forgiveness than it is to get permission.")
#     j_message = Message(room=main_room, user=grace, data='We must state relationships, not procedures.')
#     k_message = Message(room=main_room, user=balloonicorn, data="Burn everything")
#     db.session.add(a_message)
#     db.session.add(b_message)
#     db.session.add(c_message)
#     db.session.add(d_message)
#     db.session.add(e_message)
#     db.session.add(f_message)
#     db.session.add(g_message)
#     db.session.add(h_message)
#     db.session.add(i_message)
#     db.session.add(j_message)
#     db.session.add(k_message)
#     db.session.commit()
#     #TODO
#     return Message.query.all()


# #TODO: Turn these into asserts and put them into tests.py
# def test_example_data(app, db_uri):
#     '''Create example data for the test database.'''

#     connect_to_db(app, db_uri)

#     # Tests follow

#     # Reset the world
#     seed_force(app)

#     # Create and insert Users
#     # balloonicorn = db.session.query(User).get(1)
#     # # balloonicorn = User(name="Balloonicorn")
#     # grace = User(name="Grace Hopper")
#     # # db.session.add(balloonicorn)
#     # db.session.add(grace)
#     # db.session.commit()
#     test_create_get_users(app)

#     # Test user retrieval
#     # users = User.query.all()
#     # print users
#     test_get_users(app)


#     # Create and insert a room
#     # main_room = db.session.query(Room).get(1)
#     # # main_room = Room()
#     # # db.session.add(main_room)
#     # # db.session.commit()
#     # db.session.add(main_room.join_room(grace))
#     # # db.session.add(main_room.join_room(balloonicorn))
#     # db.session.commit()
#     test_join_room(app)



#     # Test room and room_user retrieval
#     # rooms = Room.query.all()
#     # room_users = RoomUser.query.all()
#     # print rooms
#     # print room_users
#     test_get_rooms(app)

#     # Create and insert Messages
#     # a_message = Message(room=main_room, user=grace, data="Please cut off a nanosecond and send it over to me")
#     # b_message = Message(room=main_room, user=grace, data='I need something to compare this to. Could I please have a microsecond?')
#     # c_message = Message(room=main_room, user=grace, data='I had a running compiler and nobody would touch it... they carefully told me, computers could only do arithmetic; they could not do programs.')
#     # d_message = Message(room=main_room, user=grace, data="I've always been more interested in the future than in the past.")
#     # e_message = Message(room=main_room, user=grace, data='Life was simple before World War II. After that, we had systems.')
#     # f_message = Message(room=main_room, user=grace, data='A ship in port is safe; but that is not what ships are built for. Sail out to sea and do new things.')
#     # g_message = Message(room=main_room, user=grace, data='The wonderful thing about standards is that there are so many of them to choose from.')
#     # h_message = Message(room=main_room, user=grace, data="In pioneer days they used oxen for heavy pulling, and when one ox couldn't budge a log, they didn't try to grow a larger ox. We shouldn't be trying for bigger computers, but for more systems of computers.")
#     # i_message = Message(room=main_room, user=grace, data="It's easier to ask forgiveness than it is to get permission.")
#     # j_message = Message(room=main_room, user=grace, data='We must state relationships, not procedures.')
#     # k_message = Message(room=main_room, user=balloonicorn, data="Burn everything")
#     # db.session.add(a_message)
#     # db.session.add(b_message)
#     # db.session.add(c_message)
#     # db.session.add(d_message)
#     # db.session.add(e_message)
#     # db.session.add(f_message)
#     # db.session.add(g_message)
#     # db.session.add(h_message)
#     # db.session.add(i_message)
#     # db.session.add(j_message)
#     # db.session.add(k_message)
#     # db.session.commit()
#     # Test retrieval
#     # messages = Message.query.all()
#     # print messages
#     test_create_get_messages(app)


#     #######
#     # Test relationships

#     print "User Messages\n=================================\n"
#     users = User.query.all()
#     for user in users:
#         print "user.messages: ", user.messages
#         print "user.rooms: ", user.rooms


#     print "\n\nRoom Messages\n=================================\n"
#     rooms = Room.query.all()
#     for room in rooms:
#         print "room.messages: ", room.messages
#         print "room users: ", room.users


#     print "\n\nAssociations\n=================================\n"
#     room_users = RoomUser.query.all()
#     for room_user in room_users:
#         print "room_user: ", room_user
#====

if __name__ == "__main__":
    unittest.main()
