**README**
Minimalistic honeypot server. 

Features:
- HTTP default answer
- Process big file and extract intel
- SMTP support [ % ]
- DNS support [ % ]
- Listen on multiple ports [ % ]



**INSTALL**
1. Activate in supervisor following code:
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



