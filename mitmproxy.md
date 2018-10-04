
```
yum install -y python-devel \
libffi-devel \
openssl-devel \
libxml2-devel \
libxslt-devel \
libjpeg-devel \
zlib zlib-devel \
gcc

virtualenv proxy
source proxy/bin/activate
pip install mitmproxy==0.18.2
```

```
docker run --rm -it -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -p 8080:8080 mitmproxy/mitmproxy
```
