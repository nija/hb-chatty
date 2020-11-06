# pylint: disable=I0011,C0103
from event import Event
from bus import Bus
from listener import SparkleBot
import os
import re
import urllib
from weather_api import WeatherAPI

# 1- Register listeners on the bus
bot_name = 'Pyro'
location = "Mountain View, CA, USA"
bus = Bus()
bus.register(SparkleBot(bot_name, bus=bus, user_id=8), Event.Types.message_created_event)

# 2- Let's create some events on the bus and see if our listeners pick them up
num = 4
for i in range(num):
    if i % num == 0:
        print "throwing message_created_event - weather"
        bus.notify(Event(Event.Types.message_created_event, {"room_id":1, "data": "{} weather {}".format(bot_name, location), "user_id": 2, "user_name": "Anony Mouse"}))
    elif i % num == 1:
        print "throwing message_created_event - help"
        bus.notify(Event(Event.Types.message_created_event, {"room_id":1, "data": "{} help".format(bot_name), "user_id": 2, "user_name": "Anony Mouse"}))
    elif i % num == 2:
        print "throwing message_created_event - story"
        bus.notify(Event(Event.Types.message_created_event, {"room_id":1, "data": "{} story".format(bot_name), "user_id": 2, "user_name": "Anony Mouse"}))
    else:
        print "throwing user_joins_room_event"
        bus.notify(Event(Event.Types.user_joins_room_event, {}))
