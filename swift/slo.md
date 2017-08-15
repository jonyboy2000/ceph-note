

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
#curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/container1/test?multipart-manifest=put' -X PUT -H "Accept-Encoding: gzip" -H "X-Auth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979" --data-binary @manifest.json


#curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/c1/1.txt' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979"
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
# curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/c2/2.txt' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979"
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

```
[root@yly-swift ~]# curl -i 'http://127.0.0.1:8080/v1/TEMPAUTH_swiftprojecttest1/container1/test?multipart-manifest=get' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: TEMPAUTH_tk2560a95287ea4f83bf3dd1c855c75979"
HTTP/1.1 200 OK
Content-Length: 312
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 15:15:34 GMT
Etag: f3c06728d27a31df9135cd48564c9e3d
X-Timestamp: 1502810133.87572
X-Static-Large-Object: True
Content-Type: application/json; charset=utf-8
X-Trans-Id: tx491d326dd26b479bb9373-005993223c
X-Openstack-Request-Id: tx491d326dd26b479bb9373-005993223c
Date: Tue, 15 Aug 2017 16:33:00 GMT

[{"hash": "77a319564621b96fa0656e24c67960ef", "last_modified": "2017-08-15T15:10:07.000000", "bytes": 7, "name": "/c1/1.txt", "content_type": "text/plain"}, {"hash": "d0284d48bae75d56a8d372ea361f4876", "last_modified": "2017-08-15T15:10:15.000000", "bytes": 7, "name": "/c2/2.txt", "content_type": "text/plain"}]


[root@yly-swift ~]# swift -A http://localhost:8080/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3 stat  container1 test
               Account: TEMPAUTH_swiftprojecttest1
             Container: container1
                Object: test
          Content Type: application/x-www-form-urlencoded
        Content Length: 14
         Last Modified: Tue, 15 Aug 2017 15:15:34 GMT
                  ETag: "7e1dd2cafba200f8cca88daac07dc883"
         Accept-Ranges: bytes
           X-Timestamp: 1502810133.87572
            X-Trans-Id: tx56e667d0f5e8441aa5652-005993232b
 X-Static-Large-Object: True
X-Openstack-Request-Id: tx56e667d0f5e8441aa5652-005993232b
```



# ceph
```
[root@ceph77 ~]# swift -A http://localhost:80/auth/v1.0 -U swiftprojecttest1:swiftusertest3 -K testing3  stat  s003 4byte
                 Account: v1
               Container: s003
                  Object: 4byte
            Content Type: binary/octet-stream
          Content Length: 5
           Last Modified: Tue, 15 Aug 2017 16:28:48 GMT
                    ETag: "d5de645a390e5b932bce6950487b8e1b"
              Meta Mtime: 1502814499.697179
Meta Static-Large-Object:
           Accept-Ranges: bytes
              Connection: Keep-Alive
             X-Timestamp: 1502814528.36418
              X-Trans-Id: tx000000000000000163bb4-00599322eb-1120-default
   X-Static-Large-Object: True
```


```
[root@ceph77 ~]# curl -i 'http://localhost/swift/v1/s003/4byte?multipart-manifest=get' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: AUTH_rgwtk20000000737769667470726f6a65637474657374313a7377696674757365727465737433a7b1e2b15fbcc5f80c679459eda8371440490cd116dfe1bc04934e1bb437742fca9c99aa"
HTTP/1.1 200 OK
Content-Length: 0
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 16:28:48 GMT
X-Timestamp: 1502814528.36418
etag: cf551d171f3374fc07c5cd57f6c87a78
X-Object-Meta-Mtime: 1502814499.697179
X-Object-Meta-Static-Large-Object:
X-Trans-Id: tx000000000000000163ba4-00599321e0-1120-default
Content-Type: binary/octet-stream
Date: Tue, 15 Aug 2017 16:31:28 GMT


[root@ceph77 ~]# curl -i 'http://localhost/swift/v1/s003/4byte' -X GET -H "Accept-Encoding: gzip" -H "X-Auth-Token: AUTH_rgwtk20000000737769667470726f6a65637474657374313a7377696674757365727465737433a7b1e2b15fbcc5f80c679459eda8371440490cd116dfe1bc04934e1bb437742fca9c99aa"
HTTP/1.1 200 OK
Content-Length: 5
Accept-Ranges: bytes
Last-Modified: Tue, 15 Aug 2017 16:28:48 GMT
X-Timestamp: 1502814528.36418
X-Static-Large-Object: True
etag: "d5de645a390e5b932bce6950487b8e1b"
X-Object-Meta-Mtime: 1502814499.697179
X-Object-Meta-Static-Large-Object:
X-Trans-Id: tx000000000000000163ba7-00599322a6-1120-default
Content-Type: binary/octet-stream
Date: Tue, 15 Aug 2017 16:34:46 GMT

1234

```

