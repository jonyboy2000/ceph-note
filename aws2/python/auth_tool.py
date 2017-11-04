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



class S3Auth():
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

    def __init__(self, access_key, secret_key, service_url=None, url=None, headers={},method='GET'):
        if service_url:
            self.service_base_url = service_url
        self.access_key = str(access_key)
        self.secret_key = str(secret_key)
        self.headers = headers
        self.url = url
        self.method = method

    def sign(self):
        # Create date header if it is not created yet.
        if 'date' not in self.headers and 'x-amz-date' not in self.headers:
            self.headers['date'] = formatdate(
                timeval=None,
                localtime=False,
                usegmt=True)
        signature = self.get_signature()
        if py3k:
            signature = signature.decode('utf-8')
        self.headers['Authorization'] = 'AWS %s:%s' % (self.access_key, signature)
        return self

    def get_signature(self):
        canonical_string = self.get_canonical_string(
            self.url, self.headers, self.method)
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


url='/test1/1.txt'
a = S3Auth('onest', 'onest', service_url='zgp2z1.ecloud.today',url=url, headers={
                                                                           'X-Amz-Date': 'Sat, 04 Nov 2017 07:47:41 GMT',
                                                                           'X-Amz-User-Agent':'aws-sdk-js/2.100.0 callback',
                                                                           'Content-Type': 'text/plain'
                                                                           },method='PUT').sign()
print a.headers['Authorization']

raw='''
Accept:*/*
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Authorization:AWS onest:O3QnkuFZfPgbys33XHduZSvzcPg=
Connection:keep-alive
Content-Length:0
Content-Type:text/plain
DNT:1
Host:zgp2z1.ecloud.today
Origin:null
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36
X-Amz-Date:Sat, 04 Nov 2017 07:47:41 GMT
X-Amz-User-Agent:aws-sdk-js/2.100.0 callback
'''

# import requests
# import logging
# from requests_toolbelt.utils import dump
# logging.basicConfig(level=logging.DEBUG)
# response = requests.put(url,headers= a.headers)
# data = dump.dump_all(response)
# print(data.decode('utf-8'))
