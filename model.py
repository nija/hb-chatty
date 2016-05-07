from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AbstractAction(db.Model):
    '''This is a placeholder'''

    # __tablename__ = "games"
    # game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(20), nullable=False, unique=True)
    # description = db.Column(db.String(100))

class Logs(AbstractAction):
    '''This is a placeholder'''

class Messages(AbstractAction):
    '''This is a placeholder'''

class Rooms(db.Model):
    '''This is a placeholder'''

class Users(db.Model):
    '''This is a placeholder'''


def connect_to_db(app, db_uri="postgresql:///chatty"):
    '''Configure the database connection'''
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    '''Create example data for the test database.'''
    '''This is a placeholder'''
    
    # test_game_1 = Game(name="Code Names",
    #                    description="Give each other codes names and run around pretending to be spies.")
    # test_game_2 = Game(name="Apples to Apples",
    #                    description="Team charades")
    # db.session.add(test_game_1)
    # db.session.add(test_game_2)
    # db.session.commit()


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print "Connected to DB."
