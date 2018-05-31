# -*- coding: utf-8 -*-
import hmac

from hashlib import sha1 as sha

py3k = False
try:
    from urlparse import urlparse, unquote
    from base64 import encodestring
except:
    py3k = True
    from urllib.parse import urlparse, unquote
    from base64 import encodebytes as encodestring

from email.utils import formatdate

from requests.auth import AuthBase


class S3Auth(AuthBase):
    """Attaches AWS Authentication to the given Request object."""

    service_base_url = 's3.amazonaws.com'
    # List of Query String Arguments of Interest
    special_params = [
        'acl', 'location', 'logging', 'partNumber', 'policy', 'requestPayment',
        'torrent', 'versioning', 'versionId', 'versions', 'website', 'uploads',
        'uploadId', 'response-content-type', 'response-content-language',
        'response-expires', 'response-cache-control', 'delete', 'lifecycle',
        'response-content-disposition', 'response-content-encoding', 'tagging',
        'notification', 'cors', 'syncing'
    ]

    def __init__(self, access_key, secret_key, service_url=None):
        if service_url:
            self.service_base_url = service_url
        self.access_key = str(access_key)
        self.secret_key = str(secret_key)

    def __call__(self, r):
        # Create date header if it is not created yet.
        if 'date' not in r.headers and 'x-amz-date' not in r.headers:
            r.headers['date'] = formatdate(
                timeval=None,
                localtime=False,
                usegmt=True)
        signature = self.get_signature(r)
        if py3k:
            signature = signature.decode('utf-8')
        r.headers['Authorization'] = 'AWS %s:%s' % (self.access_key, signature)
        return r

    def get_signature(self, r):
        canonical_string = self.get_canonical_string(
            r.url, r.headers, r.method)
        if py3k:
            key = self.secret_key.encode('utf-8')
            msg = canonical_string.encode('utf-8')
        else:
            key = self.secret_key
            msg = canonical_string
        h = hmac.new(key, msg, digestmod=sha)
        return encodestring(h.digest()).strip()

    def get_canonical_string(self, url, headers, method):
        parsedurl = urlparse(url)
        objectkey = parsedurl.path[1:]
        query_args = sorted(parsedurl.query.split('&'))

        bucket = parsedurl.netloc[:-len(self.service_base_url)]
        if len(bucket) > 1:
            # remove last dot
            bucket = bucket[:-1]

        interesting_headers = {
            'content-md5': '',
            'content-type': '',
            'date': ''}
        for key in headers:
            lk = key.lower()
            try:
                lk = lk.decode('utf-8')
            except:
                pass
            if headers[key] and (lk in interesting_headers.keys()
                                 or lk.startswith('x-amz-')):
                interesting_headers[lk] = headers[key].strip()

        # If x-amz-date is used it supersedes the date header.
        if not py3k:
            if 'x-amz-date' in interesting_headers:
                interesting_headers['date'] = ''
        else:
            if 'x-amz-date' in interesting_headers:
                interesting_headers['date'] = ''

        buf = '%s\n' % method
        for key in sorted(interesting_headers.keys()):
            val = interesting_headers[key]
            if key.startswith('x-amz-'):
                buf += '%s:%s\n' % (key, val)
            else:
                buf += '%s\n' % val

        # append the bucket if it exists
        if bucket != '':
            buf += '/%s' % bucket

        # add the objectkey. even if it doesn't exist, add the slash
        buf += '/%s' % objectkey

        params_found = False

        # handle special query string arguments
        for q in query_args:
            k = q.split('=')[0]
            if k in self.special_params:
                buf += '&' if params_found else '?'
                params_found = True

                try:
                    k, v = q.split('=', 1)

                except ValueError:
                    buf += q
                else:
                    buf += '{key}={value}'.format(key=k, value=unquote(v))

        return buf


import requests
import logging
from requests_toolbelt.utils import dump
logging.basicConfig(level=logging.DEBUG)
access_key = 'admin'
secret_key = 'admin'
url = 'http://10.254.3.68/admin/user?info&uid=yly&stats=True&format=json'
response = requests.get(url, auth=S3Auth(access_key, secret_key,service_url='10.254.3.68'))
data = dump.dump_all(response)
print(data.decode('utf-8'))


#DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 10.254.3.68
#DEBUG:urllib3.connectionpool:http://10.254.3.68:80 "GET /admin/user?info&uid=yly&stats=True&format=json HTTP/1.1" 200 383
#< GET /admin/user?info&uid=yly&stats=True&format=json HTTP/1.1
#< Host: 10.254.3.68
#< Connection: keep-alive
#< Accept-Encoding: gzip, deflate
#< Accept: */*
#< User-Agent: python-requests/2.18.4
#< date: Thu, 31 May 2018 08:03:03 GMT
#< Authorization: AWS admin:6xwI7cGF0IWpFPGoxtlu1XsNT/s=
#<

#> HTTP/1.1 200 OK
#> x-amz-request-id: tx00000000000000000092e-005b0fac37-ac29c-default
#> Content-Length: 383
#> Date: Thu, 31 May 2018 08:03:03 GMT
#> Connection: Keep-Alive
#>
#{"tenant":"","user_id":"yly","display_name":"yly","email":"","suspended":0,"max_buckets":1000,"subusers":[{"id":"yly:swift","permissions":"full-control"}],"keys":[{"user":"yly","access_key":"yly","secret_key":"yly"}],"swift_keys":[{"user":"yly:swift","secret_key":"oxnewNiNOZfatKqmXqkHnZbGDFW9vCnU0Ps4t15q"}],"caps":[],"stats":{"num_kb":20999,"num_kb_rounded":21020,"num_objects":8}}



