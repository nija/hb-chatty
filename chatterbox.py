

class Chattybot(object):
    """Docstring for Chatterbox"""
    def __init__(self, name, server_uri):
        self.name = name
        self.server_uri = server_uri
        self.last_updated = 0


    def get_chat_history_by_time(self):
        '''Checks for a new chat message'''
        # if there is a new messages, parse it

    def parse_chat_message(self, json_message):
        '''Takes a single JSON messages and acts upon it'''

    def post_chat_message(self, chat_message):
        '''Takes in a string to post'''

if __name__ == "__main__":
    '''polling occurs here'''
    chatty = Chattybot("chatter", "http://localhost:5001")
    
