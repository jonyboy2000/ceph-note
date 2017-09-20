#!/usr/bin/env bash
KEY_ID=cosbench
KEY_SECRET=cosbench
DATE=`date -u -R`

BUCKET="website01"
contentType=""
ContentMD5=""
x_amz_acl="public-read"

stringToSign="PUT\n${ContentMD5}\n${contentType}\n${DATE}\nx-amz-acl:${x_amz_acl}\n/$BUCKET/?acl"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${KEY_SECRET} -binary | base64`

HOST="127.0.0.1:7480/website01"
uri="http://${HOST}/?acl"

curl -s -v -X PUT ${uri} \
-H "Authorization: AWS ${KEY_ID}:${signature}" \
-H "Date: ${DATE}" \
-H "Host: ${HOST}" \
-H "Content-Type: ${contentType}" \
-H "x-amz-acl: ${x_amz_acl}"
