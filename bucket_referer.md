```
#设置防盗链
ceph-request put '/test2/?referer' -c user1.request  --file referer.xml

#下载对象
curl -v http://127.0.0.1:7480/test2/1.txt --header "referer: http://aliyun1.com"
```

referer.xml 
```
<RefererConfiguration><AllowEmptyReferer>true</AllowEmptyReferer><RefererList><Referer>http://aliyun.com</Referer><Referer>http://*.aliyuncs.com</Referer></RefererList></RefererConfiguration>
```
