
```
sudo mkdir -p /var/lib/ceph/radosgw/ceph-rgw.rgw5
sudo ceph-authtool /var/lib/ceph/radosgw/ceph-rgw.rgw5/keyring -n client.rgw.rgw5 --gen-key   --create-keyring
sudo chown ceph:ceph -R  /var/lib/ceph/radosgw/ceph-rgw.rgw5
sudo ceph-authtool -n client.rgw.rgw5 --cap mon 'allow rw'  --cap osd 'allow rwx' /var/lib/ceph/radosgw/ceph-rgw.rgw5/keyring
sudo ceph -k /etc/ceph/ceph.client.admin.keyring auth add client.rgw.rgw5 -i /var/lib/ceph/radosgw/ceph-rgw.rgw5/keyring



sudo mkdir -p /var/lib/ceph/radosgw/ceph-rgw.rgw5
sudo ceph auth get client.rgw.rgw5 -o  /var/lib/ceph/radosgw/ceph-rgw.rgw5/keyring
sudo chown ceph:ceph -R  /var/lib/ceph/radosgw/ceph-rgw.rgw5
```
