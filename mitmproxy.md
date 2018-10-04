
```
virtualenv proxy
source proxy/bin/activate
pip install mitmproxy==0.18.2
```

```
docker run --rm -it -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy -p 8080:8080 mitmproxy/mitmproxy
```
