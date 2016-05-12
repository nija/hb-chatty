create table rooms (
	room_id serial primary key
	)

create table users (
	user_id serial primary key
	)

create table messages (
	message_id serial primary key
	data varchar(2048)
	time_stamp  
    # action_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # data = db.Column(db.String(2048))
    # timestamp = db.Column(db.Datetime, nullable=False)
    # expiry = db.Column(db.Datetime)
    # FKEY user_id = db.Column(db.Integer)
	)

create table rooms_users_association(
	rooms_users_association_id serial primary key
	room_id )