# PicappAppServer

## Status
[![Build Status](https://travis-ci.com/RodrigoDeRosa/PicappAppServer.svg?token=rEyCUWQVS9saEunkyMqa&branch=master)](https://travis-ci.com/RodrigoDeRosa/PicappAppServer)

## Installation and usage
In order to install and run the AppServer as local inside a virtualenv, simply clone this repository and run:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ gunicorn 'src.main:run_app(local=True,external_server=True)' --log-file=-

To deactivate the virtual env, simply type in the same terminal:

    $ deactivate

## Docker
In order to run the server locally via Docker, you need to install both
[docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/).

Once you have both of them, you can get the server running by opening a
console and executing:

    $ <path-to-project-folder>/startup
    
And this one will start listening on [localhost:5000](https://localhost:5000).
You can stop it anytime by running:

    $ <path-to-project-folder>/shutdown


**NOTES:**

To run this Shell scripts, you will need to give them execution permission with
the command:

    $ chmod +x startup
    $ chmod +x shutdown

Also, they run 'sudo' commands so you will be asked for super user password.
    
## Heroku
![Heroku](https://heroku-badge.herokuapp.com/?app=picapp-app-server&root=/users)

Heroku is integrated automatically via GitHub. Every time we update master branch,
Heroku builds and deploys the last version.

## Code coverage
[![codecov](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer/branch/master/graph/badge.svg?token=z6KQ00Bcth)](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer)

By clicking on the badge, you can see the code coverage report.

## API
 
You can see the interface of this Application Server
[here](https://app.swaggerhub.com/apis/SteelSoft/PicApp-AppServer-Final/1.0).

## Testing script

First, execution permission must be given through:

    $ chmod +x tstthis

Then it can be used this way:

* **./tstthis unit** runs unit tests
* **./tstthis api local** runs api (semi-e2e) tests against a local, running appserver
* **./tstthis api heroku** runs api (semi-e2e) tests against the heroku-hosted appserver

Note that API tests require the heroku-hosted shared server to be running, hence also need an internet connection.



