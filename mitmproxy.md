
```
yum install -y python-devel libffi-devel openssl-devel libxml2-devel libxslt-devel libjpeg-devel zlib zlib-devel gcc

virtualenv proxy
source proxy/bin/activate
pip install mitmproxy==0.18.2
pip install https://files.pythonhosted.org/packages/0b/37/d1ce84f4fde4d52a070bed414c7696162a43f3b5454fe5b3154968f17d14/mitmproxy-0.18.2-py2.py3-none-any.whl
```

代理s3
```
./proxy/bin/mitmproxy -R http://127.0.0.1:7480 --insecure -p 8080 --setheader :~q:Host:127.0.0.1:8080
./proxy/bin/mitmdump -d  -R http://127.0.0.1:7480 --insecure -p 8080 --setheader :~q:Host:127.0.0.1:8080
```

```
docker run --rm -it -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -p 8080:8080 mitmproxy/mitmproxy
```


