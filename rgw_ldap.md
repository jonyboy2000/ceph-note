

```
#安装ldap服务器
yum install -y openldap-clients openldap-servers 

#拷贝配置文件
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG && chown ldap:ldap /var/lib/ldap/DB_CONFIG 

#启动服务
systemctl start slapd 

#用密码工具生成ldap密码
[root@yly-ldap ~]# slappasswd   #输入onest123
New password:
Re-enter new password:
{SSHA}0GIwZrxnDiBE8mfESzJlriCVIPlm8/+c  #填到下面的chrootpw.ldif文件

#*.ldif 文件作用类似mysql语句的sql文件

cat << EOF > chrootpw.ldif 
dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}0GIwZrxnDiBE8mfESzJlriCVIPlm8/+c  #onest123加密密码
EOF

#执行ldapadd命令修改ldap服务器的root密码（类似修改mysql的root密码）
ldapadd -Y EXTERNAL -H ldapi:/// -f chrootpw.ldif

#导入基本的schema,ldap中的所有记录可添加属性的描述文件，类似mysql数据库中定义记录的smallint,int这些属性的定义文件（schema文件定义smallint是多少位，最大值是多少，能否为字符串这些）

find /etc/openldap/schema/ -name "*.ldif" -exec ldapadd -Y EXTERNAL -H ldapi:/// -D "cn=config" -f {} \; 

#生成密码给一个数据库用，ldap可以有多个数据库，类似mysql可以有多个databases(mysql show databases;)

slappasswd   #输入qwe123  #填到下面的chdomain.ldif文件

#创建一个数据库 dc=onest,dc=com,登录该数据库的root账户名为 cn=admin,dc=onest,dc=com

cat << EOF > chdomain.ldif 
dn: olcDatabase={1}monitor,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth"
  read by dn.base="cn=admin,dc=onest,dc=com" read by * none 

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=onest,dc=com    

dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=admin,dc=onest,dc=com

dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}pTENOccP/gpYzqCO/CJoOvzm/R418iLj  #qwe123的加密密码，

dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange by
  dn="cn=admin,dc=onest,dc=com" write by anonymous auth by self write by * none 
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by dn="cn=admin,dc=onest,dc=com" write by * read 
EOF

ldapmodify -Y EXTERNAL -H ldapi:/// -f chdomain.ldif 

#创建组
cat << EOF > basedomain.ldif
dn: dc=onest,dc=com
objectClass: top
objectClass: dcObject
objectclass: organization
o: root_ldap
dc: onest

dn: cn=Manager,dc=onest,dc=com 
objectClass: organizationalRole
cn: Manager
description: Directory Manager

dn: ou=People,dc=onest,dc=com
objectClass: organizationalUnit
ou: People

dn: ou=Group,dc=onest,dc=com
objectClass: organizationalUnit
ou: Group
EOF 

ldapadd -x -D cn=admin,dc=onest,dc=com -W -f basedomain.ldif 

#创建ceph用户
[root@yly-ldap vstart]# python
Python 2.7.5 (default, Nov  6 2016, 00:28:07)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from passlib.hash import ldap_salted_sha1 as ssha
>>> print ssha.encrypt("thisispasswdforceph", salt_size=16)
{SSHA}oSpzFEzcz52GJcnA7sB2tmTsrQYqJYQQAsA4hxDiPAegNOY8

[root@yly-ldap ~]# cat ceph.ldif
dn: uid=ceph,ou=People,dc=onest,dc=com
uid:ceph
sn: ceph
cn: ceph
objectclass: inetOrgPerson
userPassword: {SSHA}oSpzFEzcz52GJcnA7sB2tmTsrQYqJYQQAsA4hxDiPAegNOY8   #thisispasswdforceph的加密密码

ldapadd -x -D cn=admin,dc=onest,dc=com -W -f ceph.ldif


#使用下面命令测试ceph用户是否可以连接ldap服务器
ldapsearch -x -D "uid=ceph,ou=People,dc=onest,dc=com" -W  -b "ou=People,dc=onest,dc=com" -s sub 'uid=ceph'


#修改ceph.conf使用ldap认证
rgw_ldap_secret = "/etc/bindpass"
rgw_ldap_uri = ldaps://10.139.15.173:389
rgw_ldap_binddn = "uid=ceph,ou=People,dc=onest,dc=com"
rgw_ldap_searchdn = "ou=People,dc=onest,dc=com"
rgw_ldap_dnattr = "uid"
rgw_s3_auth_use_ldap = true

echo "thisispasswdforceph" > /etc/bindpass

#使用radosgw-token生成token
[root@yly-ldap vstart]# export RGW_ACCESS_KEY_ID=ceph
[root@yly-ldap vstart]# export RGW_SECRET_ACCESS_KEY=ceph
[root@yly-ldap vstart]# radosgw-token --encode --ttype=ldap
2018-02-09 17:41:53.087027 7f7e0b6dd9c0 -1 WARNING: the following dangerous and experimental features are enabled: *
2018-02-09 17:41:53.087047 7f7e0b6dd9c0  0 lockdep start
2018-02-09 17:41:53.087408 7f7e0b6dd9c0 -1 WARNING: the following dangerous and experimental features are enabled: *
2018-02-09 17:41:53.126960 7f7e0b6dd9c0 -1 WARNING: the following dangerous and experimental features are enabled: *
ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImNlcGgiLAogICAgICAgICJrZXkiOiAiY2VwaCIKICAgIH0KfQo=
2018-02-09 17:41:53.188087 7f7e0b6dd9c0  0 lockdep stop

```

```
import base64, json
tokenjson = {}
tokenjson["RGW_TOKEN"] = {}
tokenjson["RGW_TOKEN"]['version'] = "1"
tokenjson["RGW_TOKEN"]['type'] = "ldap"
tokenjson["RGW_TOKEN"]['id'] = "ceph" #ldap用户名 dnr
tokenjson["RGW_TOKEN"]['key'] = "thisispasswdforceph" #ceph用户的 ldap密码
print base64.b64encode(json.dumps(tokenjson)) #也可以使用这个生成的token,和radosgw-token生成的不同是因为多了些\n和空格这些,json解析的时候没问题
```

测试脚本(request库)
```
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
access_key = 'ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImNlcGgiLAogICAgICAgICJrZXkiOiAiY2VwaCIKICAgIH0KfQo='
secret_key = 'xxxx'
url = 'http://127.0.0.1'
#url = 'http://127.0.0.1/ldapbucket'
response = requests.get(url, auth=S3Auth(access_key, secret_key,service_url='127.0.0.1'))
#response = requests.put(url, auth=S3Auth(access_key, secret_key,service_url='127.0.0.1'))
data = dump.dump_all(response)
print(data.decode('utf-8'))

```

boto2
```
#!/usr/bin/python
import boto
import boto.s3.connection
from boto.s3.key import Key
import os
rgw_host = "127.0.0.1"
access_key = "ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImNlcGgiLAogICAgICAgICJrZXkiOiAiY2VwaCIKICAgIH0KfQo="
secret_key = "any"

stop_at_one = False

conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = rgw_host,
port=8080,
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)

nbuckets = 0

conn.create_bucket(bucket_name="ldap_user_ceph_create_bucket02")
for bucket in conn.get_all_buckets():
        nbuckets += 1
        if stop_at_one and nbuckets > 1:
                break
        print "bucket %s" % bucket.name

print "bucket count: %d total" % (nbuckets)
```

boto3(v2认证可以,v4认证不可以,因为取不到AWSAccessKeyId)
```
from boto3.session import Session
import boto3
access_key = "ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImNlcGgiLAogICAgICAgICJrZXkiOiAiY2VwaCIKICAgIH0KfQo="
url = "http://10.139.15.173:8080"
session = Session(access_key,"")
s3_client = session.client('s3', endpoint_url=url,
        config = boto3.session.Config(
        signature_version = 's3'
    ))
print [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]
```



ldap token 解码
```
>>> a="ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImNlcGgiLAogICAgICAgICJrZXkiOiAiY2VwaCIKICAgIH0KfQo="
>>> import base64
>>> print base64.b64decode(a)
{
    "RGW_TOKEN": {
        "version": 1,
        "type": "ldap",
        "id": "ceph",
        "key": "ceph"
    }
}

```

认证逻辑

```
auth_id = s->info.args.get("AWSAccessKeyId");  获取认证header里的 AWSAccessKeyId值(有可能是ldap认证的token)

...
...

  if ((external_auth_result < 0) &&
      (store->ctx()->_conf->rgw_s3_auth_use_ldap) &&
      (! store->ctx()->_conf->rgw_ldap_uri.empty())) {

    RGW_Auth_S3::init(store);

    ldout(store->ctx(), 15)
      << __func__ << " LDAP auth uri="
      << store->ctx()->_conf->rgw_ldap_uri
      << dendl;

    RGWToken token;
    /* boost filters and/or string_ref may throw on invalid input */
    try {
      token = rgw::from_base64(auth_id); //base64解码
    } catch(...) {
      token = std::string("");
    }

    if (! token.valid()) //请求发到ladp server 认证改用户是否存在
      external_auth_result = -EACCES;
    else {
      ldout(store->ctx(), 10)
	<< __func__ << " try LDAP auth uri="
	<< store->ctx()->_conf->rgw_ldap_uri
	<< " token.id=" << token.id
	<< dendl;

      if (ldh->auth(token.id, token.key) != 0)
	external_auth_result = -EACCES;
      else {
	/* ok, succeeded */
	external_auth_result = 0;

	/* create local account, if none exists */ //如果用户在radosgw端不存在的话就创建用户
	s->user->user_id = token.id;
	s->user->display_name = token.id; // cn?
	int ret = rgw_get_user_info_by_uid(store, s->user->user_id, *(s->user));
	if (ret < 0) {
	  ret = rgw_store_user_info(store, *(s->user), nullptr, nullptr,
				    real_time(), true);
	  if (ret < 0) {
	    dout(10) << "NOTICE: failed to store new user's info: ret=" << ret
		     << dendl;
	  }
	}

      /* set request perms */
      s->perm_mask = RGW_PERM_FULL_CONTROL;
      } /* success */
    } /* token */
  } /* ldap */


```

```
#查看创建的用户信息，可以看到并没有access-key和secret-key
[root@yly-ldap vstart]# radosgw-admin user info --uid=ceph
2018-02-11 10:09:17.143620 7fedb263b9c0 -1 auth: unable to find a keyring on /etc/ceph/ceph.client.admin.keyring,/etc/ceph/ceph.keyring,/etc/ceph/keyring,/etc/ceph/keyring.bin: (2) No such file or directory
{
    "user_id": "ceph",
    "display_name": "ceph",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "auid": 0,
    "subusers": [],
    "keys": [],
    "swift_keys": [],
    "caps": [],
    "op_mask": "read, write, delete",
    "default_placement": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "max_size_kb": -1,
        "max_objects": -1
    },
    "temp_url_keys": []
}
```
