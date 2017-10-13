
```
集群1(master zonegroup master zone)
radosgw-admin realm  create --rgw-realm=oNest2
#realm=`radosgw-admin realm  get --rgw-realm=oNest2 |grep id| awk -F '"' '{print $4}'`
radosgw-admin zonegroup create  --rgw-zonegroup=oNest2-zgp1  --realm-id=$realm --master
radosgw-admin zone  create --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1 --realm-id=$realm  --endpoints https://zgp1z1.ecloud.today:443  --access-key admin --secret admin --master
radosgw-admin period update --commit  --rgw-realm=oNest2  --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1 --url=https://masterzone.com:443
radosgw-admin user create --uid=zone.user --display-name="Zone User" --access-key=admin --secret=admin --system --rgw-realm=oNest2  --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1

chown ceph:ceph /etc/ceph/zgp1z1.ecloud.today.pem

[client.rgw.rgw1]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z1.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=oNest2-zgp1-z1
rgw zonegroup=oNest2-zgp1
rgw realm=oNest2
rgw_dns_name = zgp1z1.ecloud.today


集群2(master zonegroup slave zone)
radosgw-admin realm pull --url=https://masterzone.com:443  --access-key=admin --secret=admin
#realm=`radosgw-admin realm  get --rgw-realm=oNest2 |grep id| awk -F '"' '{print $4}'`
radosgw-admin zone  create --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z2 --realm-id=$realm  --endpoints https://zgp1z2.ecloud.today:443 --access-key admin --secret admin
radosgw-admin period update --commit --url=https://masterzone.com:443  --rgw-realm=oNest2   --access-key=admin --secret=admin

chown ceph:ceph /etc/ceph/zgp1z2.ecloud.today.pem

[client.rgw.rgw2]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw2/keyring
rgw_frontends = "civetweb port=80+443s ssl_certificate=/etc/ceph/zgp1z2.ecloud.today.pem"
#rgw_frontends = "civetweb port=80"
rgw zone=oNest2-zgp1-z2
rgw zonegroup=oNest2-zgp1
rgw realm=oNest2
rgw_dns_name = zgp1z2.ecloud.today
```
