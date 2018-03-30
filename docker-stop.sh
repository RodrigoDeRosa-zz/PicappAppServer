#!/bin/bash
imageName=picapp-app-server
containerName=picapp-container

# Remove container if existent
echo Deleting old container ...
docker stop $containerName
docker rm $containerName

# Remove image if existent
echo Deleting old image ...
docker rmi $imageName