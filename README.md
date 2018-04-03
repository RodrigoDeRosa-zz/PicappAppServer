# PicappAppServer

## Status
[![Build Status](https://travis-ci.com/RodrigoDeRosa/PicappAppServer.svg?token=rEyCUWQVS9saEunkyMqa&branch=master)](https://travis-ci.com/RodrigoDeRosa/StoriesAppServer)

## Docker
To build the application inside Docker, we just need to execute the Shell script
called 'docker-build.sh'. To do that, the following shell command is needed:

    $ ./docker-build.sh    

This shell script deletes the old version images and containers and create a new
one for the latest application build.
    
**NOTE:** You have to give execution permission to that Shell script first. That
can be done by running the following command in the console:

    $ chmod +x docker-build.sh
    
## Heroku
![Heroku](https://heroku-badge.herokuapp.com/?app=picapp-app-server&root=/)

Heroku is integrated automatically via GitHub. Every time we update master branch,
Heroku builds and deploys the last version.

## Code coverage
[![codecov](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer/branch/master/graph/badge.svg?token=z6KQ00Bcth)](https://codecov.io/gh/RodrigoDeRosa/PicappAppServer)

By clicking on the badge, you can see the code coverage report.