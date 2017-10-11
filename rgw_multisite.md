
```
集群1(master zonegroup master zone)
radosgw-admin realm  create --rgw-realm=oNest2
radosgw-admin zonegroup create  --rgw-zonegroup=oNest2-zgp1  --realm-id=ce8e5f88-0571-436f-ab68-ffe55f84eb09 --master
radosgw-admin zone  create --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1 --realm-id=ce8e5f88-0571-436f-ab68-ffe55f84eb09  --endpoints https://zgp1z1.ecloud.today:443  --access-key admin --secret admin --master
radosgw-admin period update --commit  --rgw-realm=oNest2  --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1
radosgw-admin user create --uid=zone.user --display-name="Zone User" --access-key=admin --secret=admin --system --rgw-realm=oNest2  --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z1


集群2(master zonegroup slave zone)
radosgw-admin realm pull --url=http://10.139.12.116  --access-key=admin --secret=admin
radosgw-admin zone  create --rgw-zonegroup=oNest2-zgp1  --rgw-zone=oNest2-zgp1-z2 --realm-id=ce8e5f88-0571-436f-ab68-ffe55f84eb09  --endpoints https://zgp1z2.ecloud.today:443 --access-key admin --secret admin
radosgw-admin period update --commit --url=http://10.139.12.116  --rgw-realm=oNest2   --access-key=admin --secret=admin
```
