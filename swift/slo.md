

# OPENSTACK SWIFT

```
swift -A http://localhost:8080/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3 post c1
swift -A http://localhost:8080/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3 post c2
swift -A http://localhost:8080/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3 upload --object-name 2.txt  c2 2.txt
swift -A http://localhost:8080/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3 upload --object-name 1.txt  c1 1.txt
```

```
# cat 1.txt
111111
[root@yly-swift ~]# cat 2.txt
222222
# cat manifest.json
[{"path": "/c1/1.txt"},
 {"path": "/c2/2.txt"}]
```
```
#curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/container1/test?multipart-manifest=put' -X PUT -H "Accept-Encoding: gzth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979" --data-binary @manifest.json
#curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/c1/1.txt' -X GET -H "Accept-Encoding: gzip" -H "X-A7ea4f83bf3dd1c855c75979"
HTTP/1.1 200 OK
Content-Length: 7
Content-Type: text/plain
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 15:10:07 GMT
Etag: 77a319564621b96fa0656e24c67960ef
X-Timestamp: 1502809806.44401
X-Object-Meta-Mtime: 1502809746.999000
X-Trans-Id: txccf5668069fc42cbae1ae-00599310c6
X-Openstack-Request-Id: txccf5668069fc42cbae1ae-00599310c6
Date: Tue, 15 Aug 2017 15:18:30 GMT

111111
# curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/c2/2.txt' -X GET -H "Accept-Encoding: gzip" -H "X-A7ea4f83bf3dd1c855c75979"
HTTP/1.1 200 OK
Content-Length: 7
Content-Type: text/plain
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 15:10:15 GMT
Etag: d0284d48bae75d56a8d372ea361f4876
X-Timestamp: 1502809814.30349
X-Object-Meta-Mtime: 1502809753.684000
X-Trans-Id: tx8f6274e92ffc40b19045a-00599310ce
X-Openstack-Request-Id: tx8f6274e92ffc40b19045a-00599310ce
Date: Tue, 15 Aug 2017 15:18:38 GMT

222222

# curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/container1/test' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979"
HTTP/1.1 200 OK
Content-Length: 14
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 15:15:34 GMT
Etag: "7e1dd2cafba200f8cca88daac07dc883"
X-Timestamp: 1502810133.87572
X-Static-Large-Object: True
Content-Type: application/x-www-form-urlencoded
X-Trans-Id: txa9aad239e42f4b42afebf-00599310d1
X-Openstack-Request-Id: txa9aad239e42f4b42afebf-00599310d1
Date: Tue, 15 Aug 2017 15:18:41 GMT

111111
222222
```
