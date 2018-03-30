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

# Build image
echo Build image ...
docker build -t $imageName:latest .

# Create container and run
echo Run new container ...
docker run -d -p 8080:8080 --name $containerName $imageName
