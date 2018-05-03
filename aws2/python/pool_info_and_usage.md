定时查询集群的存储pool信息和请求次数和流量信息

```
# -*- coding: UTF-8 -*-
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from boto3.session import Session
import boto3
import time
import json

import requests
import xmltodict
from xmltodict import parse, unparse, OrderedDict
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

from datetime import datetime, timedelta
from urllib import quote
import requests

pool_info_url = "http://172.20.254.48:6066/api/v0.1/osd/df.json?output_method=tree"
usage_info_url = "/admin/usage?format=json&uid=%s&start=%s&end=%s&show-entries=True&show-summary=True"
usage_info_url_all = "/admin/usage?format=json&start=%s&end=%s&show-entries=True&show-summary=True"
list_user_url = "/admin/metadata/user?format=json"
cluster_bucket = "info"
endpoint = "http://172.20.254.48:8083"
host = "172.20.254.48:8083"
bucket = "info"
access_key = 'C0U35K21AUK2FB0OZIH3'
secret_key = 'Av5rCC15nED5ch153bVM3gSe6QdaWwztQWlaT0eT'

def my_job():
    global endpoint
    global bucket
    global pool_info_url
    global access_key
    global secret_key
    global host
    resp = requests.get(pool_info_url)
    info = json.loads(resp.content)
    # print info
    # info[u'output'][u'summary'][u'total_kb']
    # info[u'output'][u'summary'][u'total_kb_avail']
    # info[u'output'][u'summary'][u'total_kb_used']
    msg = ''
    for node in info['output']['nodes']:
        if node['type'] == "root":
            msg += "%s>%s:%s kb %s kb_avail %s kb_used\n" % (time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime()), node['name'], node['kb'], node['kb_avail'], node['kb_used'])
    key = 'pool.{:%Y-%m-%d/%H/%M/%S}'.format(datetime.now())
    url = "%s/%s/%s" % (endpoint, bucket, key)
    response = requests.put(url, auth=S3Auth(access_key, secret_key, service_url=host),data=msg)

def get_usage():
    global access_key
    global secret_key
    global usage_info_urll
    global endpoint
    global bucket
    start = '{:%Y-%m-%d 00:00:00}'.format(datetime.now() - timedelta(hours=0 + 24, seconds=0))
    end = '{:%Y-%m-%d 00:00:00}'.format(datetime.now() - timedelta(hours=0,seconds=0))
    print "start:",start
    print "end:",end

    # url = usage_info_url % ("yly", quote(start), quote(end))
    url = usage_info_url_all % (quote(start), quote(end))
    host = "http://172.20.254.48:8083"
    response = requests.get(host + url, auth=S3Auth(access_key, secret_key, service_url='172.20.254.48:8083'))
    info = json.loads(response.content)
    ops = 0
    bytes_received = 0
    bytes_sent = 0
    for user in info[u'summary']:
        ops += user[u'total'][u'ops']
        bytes_received += user[u'total'][u'bytes_received']
        bytes_sent += user[u'total'][u'bytes_sent']
    msg = "op: %s bytes_received:%s bytes_sent:%s" % (ops, bytes_received, bytes_sent)
    key = 'usage.{:%Y-%m-%d/%H/%M/%S}'.format(datetime.now())
    url = "%s/%s/%s" % (endpoint, bucket, key)
    response = requests.put(url, auth=S3Auth(access_key, secret_key, service_url=host), data=msg)


# if __name__ == '__main__':
#     get_usage()
#     my_job()

sched = BlockingScheduler()
sched.add_job(my_job, 'interval', seconds=10)
sched.add_job(get_usage, 'interval', seconds=10)
# sched.add_job(my_job, 'cron', day_of_week='1-7', hour=0, minute=30)
# sched.add_job(get_usage, 'cron', day_of_week='1-7', hour=1, minute=0)
sched.start()
```
