# README
Minimalistic application level honeypot server. 


## Features:
- Support for HTTP protocol
- Support for SMTP protocol
- Process big file and generate analytics
- Listen on multiple ports


## Todo list:
- Separate stats per protocols [ % ]
- DNS support [ % ]


# Install
There are no external dependencies.

1. Activate in supervisor (or in some other similar software) following code:

```
[program:honeypot]
command=/usr/bin/python3 -B honeypot.py

directory=/home/user/honeypot/
user=root
numprocs=1
stdout_logfile=/tmp/honeypot-out.log
stderr_logfile=/tmp/honeypot-err.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
killasgroup=true
priority=1000
```


# Cron jobs
0 */1 * * * /bin/bash /app/processor.sh




# Docker
Running docker:

1. **Build**: 
```
docker build -t honeypot .
```

2. **Run**: 

```
docker run -p 2525:25 -p 5353:53 -p 8080:80 -p 4443:443 --name honeypot_instance --restart=always -d -t honeypot
```

or 

```
docker run -p 8080:80 --name honeypot_instance -d -t honeypot
```


3. **Bash (if you need)**: 
```
docker exec -i -t honeypot_instance /bin/bash
```

4. **Stop and remove**:
```
docker stop honeypot_instance
docker rm honeypot_instance 
docker rmi honeypot
```

5. **Logs**
```
docker logs -f honeypot_instance
```