
client.restapi
	key: AQBq+MxZ3MMCOBAA3ksexbct5mVesG0PMMvY3g==
	caps: [mon] allow rx
	caps: [osd] allow *

/usr/bin/ceph-rest-api --conf /etc/ceph/ceph.conf

[client.restapi]
keyring = /etc/ceph/ceph.client.restapi.keyring
public addr = 127.0.0.1:6066


nginx做前端
