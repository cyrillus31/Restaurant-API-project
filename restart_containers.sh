#! /bin/bash

docker rm $(docker ps -a --filter "name=1homework*" -q);
docker rmi $(docker images --filter "reference=1homework*" -q);
docker-compose up