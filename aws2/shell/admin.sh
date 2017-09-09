#!/usr/bin/env bash
KEY_ACCESS="yly"
KEY_SECRET="yly"
relativePath="/admin/usage"
cmd="${relativePath}?format=json&uid=yly&subuser=swift"
current=`TZ=GMT LANG=en_US date "+%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="GET\n\n\n${current}\n${relativePath}"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`
HOST="127.0.0.1"

curl -s -v -X GET "http://${HOST}${cmd}" \
-H "Authorization: AWS ${KEY_ACCESS}:${signature}" \
-H "Date: ${current}" \
-H "Host: ${HOST}"
