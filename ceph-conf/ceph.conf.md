```
[global]
mon_initial_members = onest
mon_host = 192.168.10.146
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
osd_crush_chooseleaf_type = 0
osd_pool_default_size = 1
osd_pool_default_min_size = 1
osd_journal_size = 100
#osd_crush_update_on_start = False #部署好后解开注释
osd_max_object_name_len = 460  #目录当磁盘  
osd_max_object_namespace_len = 64
```

```
mkdir /var/local/osd0  #有时候用户的/home目录空间比较大,osd放在/home目录下时候需要修改systemd unit文件 
参考 http://www.jianshu.com/p/d028f51cfbc2 将ProtectHome=true和ProtectSystem=full注释掉
chmod 777 -R  /var/local/osd0
ceph-deploy --overwrite-conf  osd prepare `hostname -s`:/var/local/osd0
ceph-deploy --overwrite-conf  osd activate `hostname -s`:/var/local/osd0

ceph-disk prepare `ceph-conf  --name=osd.7 --lookup osd_device` --zap-disk   --osd-uuid=`ceph-conf  --name=osd.7 --lookup osd_uuid`

chmod 755 /var/lib/ceph/radosgw/ceph-rgw.`hostname -s`
chmod 755 /var/lib/ceph/mon/ceph-`hostname -s`

#和vip混合部署的时候
[osd]
public_addr = 10.63.33.5
cluster_addr = 10.63.162.5


[client.rgw.rgw1]
rgw thread pool size = 1000
#rgw_frontends = "civetweb port=80"
rgw_frontends = "civetweb port=10.63.33.1:80+10.63.33.1:443s ssl_certificate=/etc/ceph/server.pem"
debug rgw = 20
rgw_enable_ops_log = true
rgw_enable_usage_log = true
rgw_user_quota_bucket_sync_interval = 180
rgw_user_quota_sync_interval = 600
rgw_user_quota_sync_wait_time = 600
rgw_gc_obj_min_wait = 660
rgw_gc_processor_max_time = 600
rgw_gc_processor_period = 600
rgw thread pool size = 500
rgw usage max user shards = 8
rgw data log num shards = 32
rgw dns name = eos.cloud.com
rgw_dns_s3website_name = eos-website.cloud.com
rgw_enable_static_website = true
rgw_enable_apis = s3, swift, swift_auth, admin, s3website


/usr/bin/radosgw -f --cluster ceph --name client.rgw.rgw1 --setuser ceph --setgroup ceph

openresty配置或nginx配置为rgw前端参考 [https://github.com/joke-lee/openresty-radosgw](https://github.com/joke-lee/openresty-radosgw)


admin用户

radosgw-admin user create --uid=admin --display-name=admin --access-key=admin --secret-key=admin --caps="users=*;buckets=*;metadata=*;usage=*;zone=*"
```


```
ceph-deploy mgr create `hostname -s`:x
chown ceph:ceph -R /var/lib/ceph/mgr
systemctl start ceph-mgr@x
```

