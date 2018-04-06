# PicappAppServer

## Status
[![Build Status](https://travis-ci.com/RodrigoDeRosa/PicappAppServer.svg?token=rEyCUWQVS9saEunkyMqa&branch=master)](https://travis-ci.com/RodrigoDeRosa/PicappAppServer)

## Docker
In order to run the server locally via Docker, you need to install both
[docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/).

Once you have both of them, you can get the server running by opening a
console in the project directory and running the following commands:

    $ ./docker-run.sh
    
And this one will start listening on [localhost:5000](https://localhost:5000).
You can stop it anytime with CTRL+C.

**NOTES:**

To run this Shell script, you will need to give it execution permission with
the command:

    $ chmod +x docker-run.sh

Also, it runs 'sudo' commands so you will be asked for super user password.
    
## Heroku
![Heroku](https://heroku-badge.herokuapp.com/?app=picapp-app-server&root=/users)

Heroku is integrated automatically via GitHub. Every time we update master branch,
Heroku builds and deploys the last version.

## Code coverage
[![codecov](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer/branch/master/graph/badge.svg?token=z6KQ00Bcth)](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer)

By clicking on the badge, you can see the code coverage report.

## API
 
You can see the interface of this Application Server
[here](https://app.swaggerhub.com/apis/SteelSoft/PicApp-AppServer-Checkpoint1.1/1.0.1.1).

## Branch Status

The following list indicates the development status of each branch.

 - feature_login -- _On Develop_
 - feature_myaccount_get -- _On Develop_
 - feature_token -- **WIP**
 - feature_ping -- _On Develop_
 - feature_sharedserverproxy -- **WIP**
 
**REFERENCE:**
    
    WIP: Still being worked on.
    On Develop: Work finished but on develop branch.
    Done: Work finished and on main branch.

