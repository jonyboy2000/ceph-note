
服务端:
```
proxychains yum install -y scsi-target-utils iscsi-initiator-utils
systemctl start tgtd
systemctl status tgtd

```
