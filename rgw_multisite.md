
```
集群1(master zonegroup master zone)
radosgw-admin realm  create --rgw-realm=oNest2
#realm=`radosgw-admin realm  get --rgw-realm=oNest2 |grep id| awk -F '"' '{print $4}'`
radosgw-admin zonegroup create  --rgw-zonegroup=zgp1  --realm-id=$realm --master
radosgw-admin zone  create --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1 --realm-id=$realm  --endpoints https://zgp1z1.ecloud.today:443  --access-key admin --secret admin --master
radosgw-admin period update --commit  --rgw-realm=oNest2  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1 --url=https://zgp1z1.ecloud.today:443
radosgw-admin user create --uid=zone.user --display-name="Zone User" --access-key=admin --secret=admin --system --rgw-realm=oNest2  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1

chown ceph:ceph /etc/ceph/zgp1z1.ecloud.today.pem

[client.rgw.rgw1]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z1.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=zgp1-z1
rgw zonegroup=zgp1
rgw realm=oNest2
rgw_dns_name = zgp1z1.ecloud.today


集群2(master zonegroup slave zone)
radosgw-admin realm pull --url=https://zgp1z1.ecloud.today:443  --access-key=admin --secret=admin
#realm=`radosgw-admin realm  get --rgw-realm=oNest2 |grep id| awk -F '"' '{print $4}'`
radosgw-admin zone  create --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z2 --realm-id=$realm  --endpoints https://zgp1z2.ecloud.today:443 --access-key admin --secret admin
radosgw-admin period update --commit --url=https://zgp1z1.ecloud.today:443  --rgw-realm=oNest2   --access-key=admin --secret=admin
radosgw-admin metadata sync init --rgw-realm=oNest2 --rgw-zonegroup=zgp1
chown ceph:ceph /etc/ceph/zgp1z2.ecloud.today.pem

[client.rgw.rgw2]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw2/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z2.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=zgp1-z2
rgw zonegroup=zgp1
rgw realm=oNest2
rgw_dns_name = zgp1z2.ecloud.today
```

主备zonegroup切换

```
zgp1上systemctl stop ceph-radosgw@rgw.rgw1
#查询发现master zgp1挂了
radosgw-admin sync status --rgw-realm=oNest2  --rgw-zonegroup=zgp2  --rgw-zone zgp2-z1
          realm 17fc5205-9dc4-447a-8be0-ed2ea664e739 (oNest2)
      zonegroup 3eb483e4-7ff8-4721-a602-ef2395aad936 (zgp2)
           zone 106d2702-37db-4c1c-bbf7-39480cb5d503 (zgp2-z1)
2017-10-31 10:50:17.701293 7fcda285a9c0  0 rgw meta sync: ERROR: failed to fetch mdlog info
  metadata sync syncing
                full sync: 0/64 shards
                failed to fetch local sync status: (5) Input/output error
#调整zgp1为非主
radosgw-admin zonegroup modify   --rgw-zonegroup=zgp1  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master=false
#调整zgp2为主
radosgw-admin zonegroup modify   --rgw-zonegroup=zgp2  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master
#更新period
radosgw-admin period update --commit  --rgw-realm=oNest2   --rgw-zonegroup=zgp2  --rgw-zone=zgp2-z1

radosgw-admin sync status   --rgw-realm=oNest2  --rgw-zonegroup=zgp2  --rgw-zone zgp2-z1
          realm 17fc5205-9dc4-447a-8be0-ed2ea664e739 (oNest2)
      zonegroup 3eb483e4-7ff8-4721-a602-ef2395aad936 (zgp2)
           zone 106d2702-37db-4c1c-bbf7-39480cb5d503 (zgp2-z1)
  metadata sync no sync (zone is master)


过了比较久的时间zpg1恢复了,继续当备
radosgw-admin realm pull --url=http://10.139.12.23   --access-key=admin --secret=admin
systemctl start ceph-radosgw@rgw.rgw1

过了比较久的时间zpg1恢复了,切换为主
radosgw-admin zonegroup modify  --rgw-zonegroup=zgp1  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master
radosgw-admin zonegroup modify  --rgw-zonegroup=zgp2  --realm-id=17fc5205-9dc4-447a-8be0-ed2ea664e739  --master=false
radosgw-admin period update --commit  --rgw-realm=oNest2  --rgw-zonegroup=zgp1  --rgw-zone=zgp1-z1
systemctl start ceph-radosgw@rgw.rgw1

zpg2调整为备
radosgw-admin realm pull --url=http://10.139.13.58  --access-key=admin --secret=admin 
systemctl restart ceph-radosgw@rgw.rgw1
```

