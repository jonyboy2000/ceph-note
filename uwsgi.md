


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
