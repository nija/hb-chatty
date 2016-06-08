# hb-chatty
[![Build Status](https://travis-ci.org/nija/hb-chatty.svg?branch=master)](https://travis-ci.org/nija/hb-chatty)
[![Coverage Status](https://coveralls.io/repos/github/nija/hb-chatty/badge.svg?branch=master)](https://coveralls.io/github/nija/hb-chatty?branch=master)
[![Join the chat at https://gitter.im/nija/hb-chatty](https://badges.gitter.im/nija/hb-chatty.svg)](https://gitter.im/nija/hb-chatty?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


![Chat Infra Diagram](./static/img/Chat_Infra_Transp.png "Infrastructure Diagram")

# Chatty

Chatty is a web app, created by Nija Mashruwala, which is used to chat with other users and an interactive chat bot. It is designed to mimic most enterprise production web services.

Learn more about the developer [here](https://www.linkedin.com/in/nmashruwala).

## Contents
- [Technologies Used](#technologiesused)
- [Features](#features)
- [Infrastucture](#infrastructure)
- [APIs](#apis)
- [Event Bus](#eventbus)
- [Reliability](#rely)

## <a name="technologiesused"></a>Technologies Used
- [Python](https://www.python.org/)
- [PostGreSQL](https://www.postgresql.org/)
- [Flask](http://flask.pocoo.org/)
- [Flask-SQLAlchemy](http://flask.pocoo.org/)
- [jQuery](https://jquery.com/)
- [Bootstrap](http://getbootstrap.com/)
- [Open Movie Database API](http://www.omdbapi.com/)
- [Wunderground API](https://www.wunderground.com/weather/api/)


## <a name="features"></a>Features

*Current*

- [X] REST API for all server interactions
- [X] Chatbot responds to basic politeness
- [X] Chatbot retrives weather information
- [X] Chatbot retrieves movie information
- [X] Chatbot comes with a help feature
- [X] Basic end-to-end ping-type healthcheck exists
- [X] Extensive monitoring healthcheck exists
- [X] Multiple users can interact at a time; all screens are updated in close to real-time


*Future*

- [ ] Multiprocessor web service enabled
- [ ] Users will be able to tell Chatbot to remind them of events
- [ ] Security hardening
- [ ] Front-end log in flow


## <a name="infrastructure"></a>Infrastructure
Chatty is implemented with a microservice architecture pattern, and is buzzword-compliant. Because of the uncoupled design, it's trivial to separate the event bus or chatbot for placement on external hosts, or allocate a separate process to handle each component. As the chat data is designed to be ephemeral, and the chat server will recreate the database schema when necessary, no data recovery steps are needed.

## <a name="apis"></a>APIs
Chatty has a full-featured and robust REST API, which allows for functionality not seen on the front-end GUI, command-line interactions, and development of third-party custom clients. 

The chat bot uses the Wunderground API to display weather information by zipcode and the Open Movie Database API to display movie information. The chat bot can also generate natural language stories using Markov Chains. This implementation of the chat bot draws from Alice in Wonderland and Through the Looking Glass.

## <a name="eventbus"></a>Event Bus
The chat server uses a one-way Publish-Subscribe bus to communicate events to the bot, and the bot uses the chat server's REST API to post a response. 

## <a name="rely"></a>Reliability
The web app is close to production-ready in that monitoring hooks and healthcheck hooks exist, code coverage is around 80%, and continuous integratino has been set up. The last steps are to lock down parts of the API, and set up continous deployment using Travis-CI and Heroku




