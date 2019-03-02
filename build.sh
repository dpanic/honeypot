#!/bin/bash

docker stop honeypot_instance
docker rm honeypot_instance 
docker rmi honeypot


docker build -t honeypot .

docker run -p 8080:80 --name honeypot_instance -d -t honeypot

docker logs -f honeypot_instance
