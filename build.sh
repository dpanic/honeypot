#!/bin/bash

docker stop honeypot_instance
docker rm honeypot_instance 
docker rmi honeypot


docker build -t honeypot .
docker run -p 2525:25 -p 5353:53 -p 8080:80 -p 4443:443 --name honeypot_instance --restart=always -d -t honeypot


#docker logs -f honeypot_instance