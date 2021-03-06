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
url = 'http://10.254.3.68/admin/usage?format=json&start=2018-04-25%2001:00:00&end=2018-04-26%2001:00:00&show-entries=False&show-summary=True&uid=yly'
response = requests.get(url, auth=S3Auth(access_key, secret_key,service_url='10.254.3.68'))
data = dump.dump_all(response)
print(data.decode('utf-8'))

#< GET /admin/usage?format=json&start=2018-04-25%2001:00:00&end=2018-04-26%2001:00:00&show-entries=False&show-summary=True&uid=yly HTTP/1.1
#< Host: 10.254.3.68
#< Connection: keep-alive
#< Accept-Encoding: gzip, deflate
#< Accept: */*
#< User-Agent: python-requests/2.18.4
#< date: Thu, 31 May 2018 08:07:57 GMT
#< Authorization: AWS admin:e77/X/M763hX4T6t/4DfWDOb2K0=
#<

#> HTTP/1.1 200 OK
#> x-amz-request-id: tx00000000000000000094d-005b0fad5d-ac29c-default
#> Content-Length: 1780
#> Date: Thu, 31 May 2018 08:07:57 GMT
#> Connection: Keep-Alive
#>
#{"summary":[{"user":"yly","categories":[{"category":"copy_obj","bytes_sent":327,"bytes_received":0,"ops":21,"successful_ops":12},{"category":"create_bucket","bytes_sent":57,"bytes_received":0,"ops":266,"successful_ops":265},{"category":"delete_bucket","bytes_sent":78,"bytes_received":0,"ops":266,"successful_ops":260},{"category":"delete_obj","bytes_sent":117,"bytes_received":0,"ops":80377,"successful_ops":80365},{"category":"get_acls","bytes_sent":17521314,"bytes_received":0,"ops":40003,"successful_ops":40003},{"category":"get_obj","bytes_sent":2621762563,"bytes_received":0,"ops":100064,"successful_ops":60044},{"category":"init_multipart","bytes_sent":219,"bytes_received":0,"ops":1,"successful_ops":0},{"category":"list_bucket","bytes_sent":114290110,"bytes_received":0,"ops":866,"successful_ops":865},{"category":"list_buckets","bytes_sent":20066,"bytes_received":0,"ops":272,"successful_ops":272},{"category":"put_account_metadata","bytes_sent":0,"bytes_received":0,"ops":1,"successful_ops":1},{"category":"put_acls","bytes_sent":380038,"bytes_received":0,"ops":20002,"successful_ops":20002},{"category":"put_bucket_metadata","bytes_sent":72,"bytes_received":0,"ops":75,"successful_ops":69},{"category":"put_lifecycle","bytes_sent":19,"bytes_received":0,"ops":1,"successful_ops":1},{"category":"put_obj","bytes_sent":6948,"bytes_received":87818724542,"ops":80375,"successful_ops":80366},{"category":"put_obj_metadata","bytes_sent":90,"bytes_received":0,"ops":12,"successful_ops":6},{"category":"stat_account","bytes_sent":0,"bytes_received":0,"ops":507,"successful_ops":507},{"category":"stat_bucket","bytes_sent":57,"bytes_received":0,"ops":60,"successful_ops":48}],"total":{"bytes_sent":2753982075,"bytes_received":87818724542,"ops":323169,"successful_ops":283086}}]}
