#!/usr/bin/env python
import base64, hmac, os, sha, sys, time, urllib

TWENTY_YEARS_IN_SECONDS = 60 * 60 * 24 * 365 * 20
aws_access_key_id = "WU1TB25VZPFEK78ITDXE"
aws_secret_access_key = "YgcYobc45CSWG9bheAzmAwlGmacXZkqstDsn7pbc"
resource = "/test/channel001/index.m3u8"
seconds_alive = TWENTY_YEARS_IN_SECONDS

# Computations:
expires = int(time.time()) + seconds_alive
resource = urllib.quote(resource)
raw_value = "GET\n\n\n{0}\n{1}".format(expires, resource)
signature = base64.b64encode(hmac.new(aws_secret_access_key, raw_value, sha).digest())

# Result:
print "http://192.168.153.181{0}?AWSAccessKeyId={1}&Expires={2}&Signature={3}".format(
    resource, urllib.quote(aws_access_key_id), expires, urllib.quote(signature))
