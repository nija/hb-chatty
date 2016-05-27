'''Events classes and info for events emitted'''
class Event(object):
    """Event class"""

    class Types(object):
        """Types of Event classes"""
        message_created_event = 'MESSAGE_CREATED_EVENT'
        user_joins_room_event = 'USER_JOINS_ROOM_EVENT'

    def __init__(self, event_type, data):
        self.data = data
        self.type = event_type

    def __str__(self):
        return "<{} {} : {}>".format(
            type(self).__name__, 
            self.type, 
            self.data)

    def get_data(self):
        return self.data

    def get_type(self):
        return self.type



if __name__ == '__main__':
    '''Allow interactive use of the class'''
    event1 = Event(
                   Event.Types.message_created_event,
                   {"room_id":1, "data": "Pyro weather 94301", "user_id": 123})
    event2 = Event(
                   Event.Types.user_joins_room_event, 
                   {"user_id":1, "room_id":2})
    print event1
    print event2