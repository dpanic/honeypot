# README
Minimalistic application level honeypot server. 


## Features:
- HTTP default answer
- Process big file and extract intel
- SMTP support [ % ]
- DNS support [ % ]
- Listen on multiple ports [ % ]



# Install
1. python3 -m pip install -r requirements.txt

2. Activate in supervisor (or in some other similar software) following code:

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
0 */1 * * * /bin/bash /home/user/honeypot/devops/processor.sh
