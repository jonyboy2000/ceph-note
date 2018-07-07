


api-server.ini
```
[uwsgi]
module = wsgi
chdir = /root/api-server/rtmp_s3_api
#uid = nginx
#gid = nginx
wsgi-file  = wsgi.py
callable = application
master = true
processes = 2
threads = 10
#http = 127.0.0.1:5000
#socket = 127.0.0.1:5000
socket = api-server.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

```
/usr/bin/uwsgi --ini /root/api-server/api-server.ini
```

```
yum install supervisor
```

vi /etc/supervisord.d/api-server.ini

```
[program:app]
autorestart=True
autostart=True
redirect_stderr=True
#environment=PATH="/home/app_env/bin"
command=/usr/bin/uwsgi --ini /root/api-server/api-server.ini
user=root
directory=/root/api-server/rtmp_s3_api
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 20
stdout_logfile = /tmp/api-server.log

[program:app2]
autorestart=True
autostart=True
redirect_stderr=True
#environment=PATH="/home/app_env/bin"
command=/usr/bin/uwsgi --ini /root/api-server/api-server2.ini
user=root
directory=/root/api-server/rtmp_s3_api
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 20
stdout_logfile = /tmp/api-server2.log

[program:app3]
autorestart=True
autostart=True
redirect_stderr=True
#environment=PATH="/home/app_env/bin"
command=/usr/bin/uwsgi --ini /root/api-server/api-server3.ini
user=root
directory=/root/api-server/rtmp_s3_api
stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 20
stdout_logfile = /tmp/api-server3.log
```

```
systemctl enable supervisord
systemctl start supervisord
```

nginx.conf
```
    upstream api_app {
      server unix:/root/api-server/rtmp_s3_api/api-server.sock;
      server unix:/root/api-server/rtmp_s3_api/api-server2.sock;
      server unix:/root/api-server/rtmp_s3_api/api-server3.sock;
    }

    server {
        listen       80 ;
        server_name  192.168.153.189;

        location / {
          include uwsgi_params;
          uwsgi_pass api_app;
#          uwsgi_pass unix:/root/api-server/rtmp_s3_api/api-server.sock;
        }
    }

```
