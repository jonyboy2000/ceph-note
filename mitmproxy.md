
```
yum install -y python-devel libffi-devel openssl-devel libxml2-devel libxslt-devel libjpeg-devel zlib zlib-devel gcc https://rpmfind.net/linux/centos/7.5.1804/os/x86_64/Packages/libjpeg-turbo-devel-1.2.90-5.el7.x86_64.rpm

virtualenv proxy
source proxy/bin/activate
pip install mitmproxy==0.18.2
pip install https://files.pythonhosted.org/packages/0b/37/d1ce84f4fde4d52a070bed414c7696162a43f3b5454fe5b3154968f17d14/mitmproxy-0.18.2-py2.py3-none-any.whl
```

反向代理s3
```
./proxy/bin/mitmproxy -R http://rgw_ip:7480 --insecure -p 8080 --setheader :~q:Host:nginx_ip:8080  --no-mouse
./proxy/bin/mitmdump -d -R http://rgw_ip:7480 --insecure -p 8080 --setheader :~q:Host:nginx_ip:8080  --no-mouse
```


