
```
user root;
master_process off;
daemon off;
worker_processes  1;        #nginx worker 数量
error_log logs/error.log;   #指定错误日志文件路径
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        lua_code_cache off;
        location /aaa {
            default_type text/html;
            set $backend  '';
            set $value1  'aa';
            rewrite_by_lua_file  /usr/local/openresty/nginx/conf/lua/ivr.lua;
            proxy_pass http://$backend;
        }


        location /testlocation {
            content_by_lua_block {
                local res = ngx.location.capture("/location/bucket2")
                ngx.say("status:", res.status, " response:", res.body)
            }
        }

        location ~* ^/location/(.*) {
            internal;
            set $bucket           "$1";
            set $aws_access       'yly';
            set $aws_secret       'yly';
            set_by_lua $now       "return ngx.cookie_time(ngx.time())";
            set $string_to_sign   "GET\n\n\n${now}\n/$bucket/";
            set_hmac_sha1          $aws_signature $aws_secret $string_to_sign;
            set_encode_base64      $aws_signature $aws_signature;
            proxy_set_header       Host 192.168.153.188;
            proxy_set_header       Date $now;
            proxy_set_header       Authorization "AWS $aws_access:$aws_signature";
            proxy_pass http://192.168.153.188/$bucket/;
        }
    }
}
```


```
         location /test {
              default_type "text/html";
              content_by_lua_file /usr/local/openresty/nginx/conf/lua/1.lua;
         }

```

```
local cjson = require "cjson"
local http = require 'resty.http'
local httpc = http.new()
httpc:set_timeout(500)
httpc:connect("192.168.153.181", 8001)
local aws_access = "admin"
local aws_secret_key = "admin"
local now = ngx.cookie_time(ngx.time())
local string_to_sign = "GET\n\n\n" .. now .. "\n/admin/bucket/";
local digest = ngx.hmac_sha1(aws_secret_key, string_to_sign)
local aws_signature = ngx.encode_base64(digest)
local auth_header = "AWS ".. aws_access .. ":" .. aws_signature;

bucket = ""
zonegroup = ""
endpoint = ""
for b in string.gmatch(ngx.var.host, '(%w*)%.?eos%-beijing%-1%.cmecloud%.cn') do
  bucket = b
end
local res, err = httpc:request({
    path = "/admin/bucket/?zonegroup&bucket=" .. bucket,
    headers = {
        ["Host"] = "192.168.153.181:8001",
        ["Authorization"] = auth_header,
        ["Date"] = now,
    },
})

if res.status then
  unjson = cjson.decode(res:read_body())
  zonegroup = unjson["zonegroup"]
  ngx.say(zonegroup)
end

```

```
[root@localhost build]# curl -H "host: test1.eos-beijing-1.cmecloud.cn"  127.0.0.1/test -v
* About to connect() to 127.0.0.1 port 80 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 80 (#0)
> GET /test HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> host: test1.eos-beijing-1.cmecloud.cn
>
< HTTP/1.1 200 OK
< Server: openresty/1.13.6.1
< Date: Fri, 13 Jul 2018 12:35:08 GMT
< Content-Type: text/html
< Transfer-Encoding: chunked
< Connection: keep-alive
<
zgp1
* Connection #0 to host 127.0.0.1 left intact
[root@localhost build]# curl -H "host: test2.eos-beijing-1.cmecloud.cn"  127.0.0.1/test -v
* About to connect() to 127.0.0.1 port 80 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 80 (#0)
> GET /test HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> host: test2.eos-beijing-1.cmecloud.cn
>
< HTTP/1.1 200 OK
< Server: openresty/1.13.6.1
< Date: Fri, 13 Jul 2018 12:35:14 GMT
< Content-Type: text/html
< Transfer-Encoding: chunked
< Connection: keep-alive
<
zgp2
* Connection #0 to host 127.0.0.1 left intact
[root@localhost build]# curl -H "host: test3.eos-beijing-1.cmecloud.cn"  127.0.0.1/test -v
* About to connect() to 127.0.0.1 port 80 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 80 (#0)
> GET /test HTTP/1.1
> User-Agent: curl/7.29.0
> Accept: */*
> host: test3.eos-beijing-1.cmecloud.cn
>
< HTTP/1.1 200 OK
< Server: openresty/1.13.6.1
< Date: Fri, 13 Jul 2018 12:32:45 GMT
< Content-Type: text/html
< Transfer-Encoding: chunked
< Connection: keep-alive
<
nil
* Connection #0 to host 127.0.0.1 left intact

```

test sdk (python)
```
from boto3.session import Session
import botocore
botocore.session.Session().set_debug_logger()
import boto3
access_key = "yly"
secret_key = "yly"
url = 'http://eos-beijing-1.cmecloud.cn'
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)
resp = s3_client.get_object(Bucket="test2", Key="obj22223333333333333333333333333", Range="bytes=0-10")
print resp['Body'].read()
resp = s3_client.get_object(Bucket="test1", Key="obj111111111111111111111111111", Range="bytes=0-10")
print resp['Body'].read()
```
boto3 config
```
cat ~/.aws/config
[default]
s3 =
    signature_version = s3
    addressing_style = virtual

```

ceph.conf
```
rgw_dns_name = eos-beijing-1.cmecloud.cn
```


dns config in nginx
```
cat /etc/dnsmasq.conf
resolv-file=/etc/resolv.dnsmasq.conf
strict-order
resolv-file=/etc/dnsmasq.d/resolv.dnsmasq.conf
addn-hosts=/etc/dnsmasq.d/dnsmasq.hosts
address=/eos-beijing-1.cmecloud.cn/127.0.0.1
address=/*.eos-beijing-1.cmecloud.cn/127.0.0.1
address=/192.168.153.181/192.168.153.181
```

nginx.conf
```
user root;
master_process off;
daemon off;
worker_processes  1;
error_log logs/error.log;
events {
    worker_connections 1024;
}

http {
    resolver 127.0.0.1;
    server {
        listen 80;
        lua_code_cache off;
        client_max_body_size 0;
        location / {
            set $backend  '';
            rewrite_by_lua_file  /usr/local/openresty/nginx/conf/lua/router.lua;
            proxy_pass http://$backend;
        }
    }
}

```

```
local zgp1 = "023c1d09-3429-4441-8980-ead2d3304ced"
local zgp2 = "60355b00-1920-4164-b2a5-feb05c74b886"

local function get_bucket()
  local host_m = ngx.re.match(ngx.var.host, [=[([^.]*)(.?)eos-beijing-1.cmecloud.cn$]=], "jo")
  if not host_m then
    -- HOST头是IP地址,则从uri中取桶名
    local uri_m = ngx.re.match(ngx.var.uri, "/([^/]*)[/?]*(?<remaining>.*)", "jo")
    return uri_m[1]
  else
    if host_m[1] == "" then
      -- 域名形式,桶名在域名后
      local uri_m2 = ngx.re.match(ngx.var.uri, "/([^/]*)[/?]*(?<remaining>.*)", "jo")
      return uri_m2[1]
    else
      -- 域名形式,桶名在域名前
      return host_m[1]
    end
  end
end

local function get_zonegroup(bucket)
  local cjson = require "cjson"
  local http = require 'resty.http'
  local httpc = http.new()
  httpc:set_timeout(500)
  httpc:connect("192.168.153.181", 8001) --rgw admin 地址
  local aws_access = "admin"
  local aws_secret_key = "admin"
  local now = ngx.cookie_time(ngx.time())
  local string_to_sign = "GET\n\n\n" .. now .. "\n/admin/bucket/";
  local digest = ngx.hmac_sha1(aws_secret_key, string_to_sign)
  local aws_signature = ngx.encode_base64(digest)
  local auth_header = "AWS ".. aws_access .. ":" .. aws_signature;
  local res, err = httpc:request({
      path = "/admin/bucket/?bucket=" .. bucket,
      headers = {
          ["Host"] = "192.168.153.181:8001",  --master zonegroup rgw admin 地址
          ["Authorization"] = auth_header,
          ["Date"] = now,
      },
  })
  if res.status then
    unjson = cjson.decode(res:read_body())
    return unjson["zonegroup"]
  end
end

local function get_endpoint(zonegroup)
  if zonegroup == zgp1 then
    return ngx.var.host .. ":8001"
  end
  if zonegroup == zgp2 then
    return ngx.var.host .. ":8002"
  end
end

local bucket = get_bucket()
local zonegroup 
local endpoint 

-- get from memcached
local memcached = require "resty.memcached"
local memc, err = memcached:new()
if  memc then
  memc:set_timeout(1000) -- 1 sec
  memc:set_keepalive(10000, 100)
  local ok, err = memc:connect("unix:/var/run/memcached/memcached.sock")
  if ok then
    local res, flags, err = memc:get(bucket)
    if not res then
       zonegroup = get_zonegroup(bucket)
       --ngx.log(ngx.ERR, "memc not hit: ", zonegroup)
       --ngx.log(ngx.ERR, "get_zonegroup:", zonegroup)
       if zonegroup and bucket then
         local ok, err = memc:set(bucket, zonegroup, 300)
         if not ok then
         --ngx.log(ngx.ERR, "memc set error")
         end
       end
    else
       --ngx.log(ngx.ERR, "memc hit: ", res)
       zonegroup = res
    end
  else
    zonegroup = get_zonegroup(bucket)
  end
else
  zonegroup = get_zonegroup(bucket)
end

if not zonegroup then
  --无法找到桶,是否为创建桶请求
  --ngx.log(ngx.ERR, "ngx.var.request_method:", ngx.var.request_method)
  if ngx.var.request_method == "PUT" then
    --如果是PUT请求
    ngx.req.read_body()
    local body_data = ngx.req.get_body_data() 
    --ngx.log(ngx.ERR, "body_data:", body_data)
    if body_data == '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><LocationConstraint>zgp1</LocationConstraint></CreateBucketConfiguration>'
    then
      --ngx.log(ngx.ERR, "create bucket in zgp1 " )
      zonegroup = zgp1
    end

    if body_data == '<CreateBucketConfiguration><LocationConstraint>zgp1</LocationConstraint></CreateBucketConfiguration>'
    then
      --ngx.log(ngx.ERR, "create bucket in zgp1 " )
      zonegroup = zgp1
    end

    if body_data == '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><LocationConstraint>zgp2</LocationConstraint></CreateBucketConfiguration>'
    then
      --ngx.log(ngx.ERR, "create bucket in zgp2 " )
      zonegroup = zgp2
    end

    if body_data == '<CreateBucketConfiguration><LocationConstraint>zgp2</LocationConstraint></CreateBucketConfiguration>'
    then
      --ngx.log(ngx.ERR, "create bucket in zgp2 " )
      zonegroup = zgp2
    end
  else
    --ngx.log(ngx.ERR, "(default) " )
    zonegroup = zgp1
  end
end

endpoint = get_endpoint(zonegroup)
--ngx.log(ngx.ERR, "backend: ", endpoint)
ngx.var.backend = endpoint
```


## memcached

```
proxychains yum  -y install libevent libevent-devel nc telnet  memcached lsof
mkdir -p /var/run/memcached/
memcached -m 100m -d -u root -c 8192 -s /var/run/memcached/memcached.sock -a 0666

location = /memc {
    set $memc_cmd $arg_cmd;
    set $memc_key $arg_key;
    set $memc_value $arg_val;
    set $memc_exptime $arg_exptime;
    memc_pass unix:/var/run/memcached/memcached.sock;
    #memc_pass 127.0.0.1:11211;
}

location = /memcset {
    content_by_lua '
        local memcached = require "resty.memcached"
        local memc, err = memcached:new()
        if not memc then
            ngx.say("failed to instantiate memc: ", err)
            return
        end
        memc:set_timeout(1000) -- 1 sec
        local ok, err = memc:set_keepalive(10000, 100)
        if not ok then
            ngx.say("cannot set keepalive: ", err)
            return
        end
        local ok, err = memc:connect("unix:/var/run/memcached/memcached.sock")
        if not ok then
            ngx.say("failed to connect: ", err)
            return
        end
        local ok, err = memc:set("dog", 32, 10)
        if not ok then
            ngx.say("failed to set dog: ", err)
            return
        end
        local res, flags, err = memc:get("dog")
        if err then
            ngx.say("failed to get dog: ", err)
            return
        end
    ';
}
```


