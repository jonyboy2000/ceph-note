

```
#解析 mon ip 错误
ceph-deploy new node1 --public-network "192.168.153.0/24"

ceph-deploy没有那么智能和强大,都是些python脚本,部署过程中特别是OSD阶段对文件系统相关的东西很敏感,强烈建议在准备ceph部署环境的时候就将相关的磁盘进行完全擦除:

wipefs -af /dev/sd?
dd if=/dev/zero of=/dev/sd? bs=1G count=1
# 设置gpt分区,不然prepare的时候报错
parted /dev/sd? mklabel gpt
```
