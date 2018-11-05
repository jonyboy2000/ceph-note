

```
ceph-request put "/test1/2.txt?append&position=0"  -c yly.request  --verbose --file yly.request  --header '{"Content-Type":"image/jpg"}'
< PUT /test1/2.txt?append&position=0 HTTP/1.1
< Host: 127.0.0.1:7480
< Content-Length: 68
< Accept-Encoding: gzip, deflate
< Accept: */*
< User-Agent: python-requests/2.6.0 CPython/2.7.5 Linux/3.10.0-862.14.4.el7.x86_64
< Connection: keep-alive
< date: Mon, 05 Nov 2018 05:43:43 GMT
< Content-Type: image/jpg
< Authorization: AWS yly:zi5PaA47NsACSdaUYVwceto8xHA=
<
< [s3]
host = 127.0.0.1
port = 7480
access_key = yly
secret_key = yly

> HTTP/1.1 200 OK
> Content-Length: 0
> ETag: "aa7b100e79fab17966f5ca43ee754da4"
> Accept-Ranges: bytes
> x-amz-next-append-position: 68
> x-amz-request-id: tx000000000000000000003-005bdfd88f-8531-default
> Date: Mon, 05 Nov 2018 05:43:43 GMT
> Connection: Keep-Alive
>
```

```
ceph-request head "/test1/2.txt"  -c yly.request  --verbose
< HEAD /test1/2.txt HTTP/1.1
< Host: 127.0.0.1:7480
< Accept-Encoding: gzip, deflate
< Accept: */*
< User-Agent: python-requests/2.6.0 CPython/2.7.5 Linux/3.10.0-862.14.4.el7.x86_64
< Connection: keep-alive
< date: Mon, 05 Nov 2018 05:44:20 GMT
< Authorization: AWS yly:vPmepTvfPLvS8RYa+3ty0Mz09+o=
<

> HTTP/1.1 200 OK
> Content-Length: 68
> Accept-Ranges: bytes
> Last-Modified: Mon, 05 Nov 2018 05:43:43 GMT
> x-amz-object-type: Appendable
> x-amz-next-append-position: 68
> ETag: "aa7b100e79fab17966f5ca43ee754da4"
> X-Amz-Storage-Class: STANDARD
> x-amz-request-id: tx000000000000000000004-005bdfd8b4-8531-default
> Content-Type: image/jpg
> Date: Mon, 05 Nov 2018 05:44:20 GMT
> Connection: Keep-Alive
>
```

```
ceph-request get "/test1/"  -c yly.request  --pretty
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Name>test1</Name>
  <Prefix/>
  <Marker/>
  <MaxKeys>1000</MaxKeys>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>1.txt</Key>
    <LastModified>2018-11-05T05:41:10.421Z</LastModified>
    <ETag>"33a53576842577bb95fae62c29a1221c-3"</ETag>
    <Size>204</Size>
    <StorageClass>STANDARD</StorageClass>
    <Owner>
      <ID>yly</ID>
      <DisplayName>yly</DisplayName>
    </Owner>
    <Type>Appendable</Type>
  </Contents>
  <Contents>
    <Key>2.txt</Key>
    <LastModified>2018-11-05T05:43:43.088Z</LastModified>
    <ETag>"aa7b100e79fab17966f5ca43ee754da4"</ETag>
    <Size>68</Size>
    <StorageClass>STANDARD</StorageClass>
    <Owner>
      <ID>yly</ID>
      <DisplayName>yly</DisplayName>
    </Owner>
    <Type>Appendable</Type>
  </Contents>
  <Contents>
    <Key>3.txt</Key>
    <LastModified>2018-11-05T05:45:45.739Z</LastModified>
    <ETag>"aa7b100e79fab17966f5ca43ee754da4"</ETag>
    <Size>68</Size>
    <StorageClass>STANDARD</StorageClass>
    <Owner>
      <ID>yly</ID>
      <DisplayName>yly</DisplayName>
    </Owner>
    <Type>Normal</Type>
  </Contents>
</ListBucketResult>
```
