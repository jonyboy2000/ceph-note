
```
集群1(master zonegroup master zone)
radosgw-admin realm  create --rgw-realm=default
radosgw-admin zonegroup create  --rgw-zonegroup=zgp1 --rgw-realm=default --master
radosgw-admin zone  create --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1 --rgw-realm=default --endpoints http://zgp1z1.ecloud.today  --access-key admin --secret admin --master
radosgw-admin period update --commit  --rgw-realm=default  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1 
radosgw-admin user create --uid=zone.user --display-name="Zone User" --access-key=admin --secret=admin --system --rgw-realm=default  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1

chown ceph:ceph /etc/ceph/zgp1z1.ecloud.today.pem

[client.rgw.rgw1]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z1.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=zgp1-z1
rgw zonegroup=zgp1
rgw realm=default
rgw_dns_name = zgp1z1.ecloud.today


集群2(master zonegroup slave zone)
radosgw-admin realm pull --url=http://zgp1z1.ecloud.today  --access-key=admin --secret=admin
radosgw-admin zone  create --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z2 --rgw-realm=default --endpoints http://zgp1z2.ecloud.today --access-key admin --secret admin
radosgw-admin period update --commit --url=http://zgp1z1.ecloud.today  --rgw-realm=default --rgw-zonegroup=zgp2 --rgw-zone=zgp2-z1   --access-key=admin --secret=admin
radosgw-admin metadata sync init --rgw-realm=default --rgw-zonegroup=zgp1

radosgw-admin metadata sync run --rgw-realm=default --rgw-zonegroup=zgp1
chown ceph:ceph /etc/ceph/zgp1z2.ecloud.today.pem

[client.rgw.rgw2]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw2/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z2.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=zgp1-z2
rgw zonegroup=zgp1
rgw realm=default
rgw_dns_name = zgp1z2.ecloud.today
```


```
seq 1 20  | xargs -I{} -P 10 radosgw-admin user create --uid=user{} --display-name=user{} --access-key=user{} --secret-key=user{} --rgw-zonegroup=zgp1 --rgw-zone=zgp1-z1 --rgw-realm=default -c ceph.conf



```

主备zonegroup切换

```
zgp1上systemctl stop ceph-radosgw@rgw.rgw1
#查询发现master zgp1挂了
radosgw-admin sync status --rgw-realm=default  --rgw-zonegroup=zgp2  --rgw-zone zgp2-z1
          realm 17fc5205-9dc4-447a-8be0-ed2ea664e739 (default)
      zonegroup 3eb483e4-7ff8-4721-a602-ef2395aad936 (zgp2)
           zone 106d2702-37db-4c1c-bbf7-39480cb5d503 (zgp2-z1)
2017-10-31 10:50:17.701293 7fcda285a9c0  0 rgw meta sync: ERROR: failed to fetch mdlog info
  metadata sync syncing
                full sync: 0/64 shards
                failed to fetch local sync status: (5) Input/output error
#调整zgp1为非主(zgp2上执行)
radosgw-admin zonegroup modify --rgw-zonegroup=zgp1 --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739 --master=false
#调整zgp2为主(zgp2上执行)
radosgw-admin zonegroup modify --rgw-zonegroup=zgp2 --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739 --master
#更新period(zgp2上执行)
radosgw-admin period update --commit  --rgw-realm=default   --rgw-zonegroup=zgp2  --rgw-zone=zgp2-z1

radosgw-admin sync status   --rgw-realm=default  --rgw-zonegroup=zgp2  --rgw-zone zgp2-z1
          realm 17fc5205-9dc4-447a-8be0-ed2ea664e739 (default)
      zonegroup 3eb483e4-7ff8-4721-a602-ef2395aad936 (zgp2)
           zone 106d2702-37db-4c1c-bbf7-39480cb5d503 (zgp2-z1)
  metadata sync no sync (zone is master)


过了比较久的时间zpg1恢复了,继续当备
radosgw-admin realm pull --url=http://10.139.12.23   --access-key=admin --secret=admin
systemctl start ceph-radosgw@rgw.rgw1

过了比较久的时间zpg1恢复了,切换为主
radosgw-admin zonegroup modify  --rgw-zonegroup=zgp1  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master
radosgw-admin zonegroup modify  --rgw-zonegroup=zgp2  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master=false
radosgw-admin period update --commit  --rgw-realm=default  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1
systemctl start ceph-radosgw@rgw.rgw1

zpg2调整为备
radosgw-admin realm pull --url=http://10.139.13.58  --access-key=admin --secret=admin 
systemctl restart ceph-radosgw@rgw.rgw1
```


```
#!/usr/bin/python
# -*- coding: utf-8 -*-

# yum install gcc python-crypto python-paramiko python-devel -y

import paramiko
import json

def ssh2(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read()
        ssh.close()
        return output
    except:
        print '%stErrorn' % (ip)


master_zgp_ip = '10.139.12.23'
master_zgp_user_ssh = 'root'
master_zgp_user_ssh_pw = 'jGs*Z+ZQ94TY9T/z'

slave_zgp_ip = '10.139.13.58'
slave_zgp_user_ssh = 'root'
slave_zgp_user_ssh_pw = 'jGs*Z+ZQ94TY9T/z'

realm = 'default'

realm_id = ssh2(master_zgp_ip, master_zgp_user_ssh, master_zgp_user_ssh_pw,
                '''radosgw-admin realm  get --rgw-realm='''+realm +''' |grep id| awk -F '"' '{print $4}' ''')
if realm_id is None:
    exit(0)
else:
    realm_id = realm_id.rstrip()

period = ssh2(master_zgp_ip, master_zgp_user_ssh, master_zgp_user_ssh_pw,
              'radosgw-admin period  get --realm-id=%s' % (realm_id,)).rstrip()
period_json = json.loads(period)
period_map = period_json['period_map']
realm_name = period_json['realm_name']

master_zonegroup = {}
slave_zonegroup = {}

for zonegroup in period_map['zonegroups']:
    print zonegroup
    print zonegroup['is_master']
    if zonegroup['is_master'] == 'true':
        master_zonegroup['api_name'] = zonegroup['api_name']
        master_zonegroup['id'] = zonegroup['id']
        master_zonegroup['master_zone'] = zonegroup['master_zone']
        master_zonegroup['zone_name'] = zonegroup['zones'][0]['name']
    else:
        slave_zonegroup['api_name'] = zonegroup['api_name']
        slave_zonegroup['id'] = zonegroup['id']
        slave_zonegroup['master_zone'] = zonegroup['master_zone']
        slave_zonegroup['zone_name'] = zonegroup['zones'][0]['name']

cmd = "radosgw-admin zonegroup modify --rgw-zonegroup=%s --realm-id=%s --master=false" % (
master_zonegroup['api_name'], realm_id,)
print cmd
ssh2(slave_zgp_ip, slave_zgp_user_ssh, slave_zgp_user_ssh_pw, cmd).rstrip()

cmd = "radosgw-admin zonegroup modify --rgw-zonegroup=%s --realm-id=%s --master" % (
slave_zonegroup['api_name'], realm_id,)
print cmd
ssh2(slave_zgp_ip, slave_zgp_user_ssh, slave_zgp_user_ssh_pw, cmd).rstrip()

cmd = "radosgw-admin period update --commit --rgw-realm=%s --rgw-zonegroup=%s --rgw-zone=%s" % (
realm_name, slave_zonegroup['api_name'], slave_zonegroup['zone_name'],)
print cmd
ssh2(slave_zgp_ip, slave_zgp_user_ssh, slave_zgp_user_ssh_pw, cmd).rstrip()
```

