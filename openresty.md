
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
