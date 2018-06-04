# ceph-deply 部署 单节点ceph集群

## 1.配置yum源

```
yum install createrepo

mkdir ceph-yum
cd ceph-yum
上传ceph rpm包到该目录
createrepo ceph-yum

python -m SimpleHTTPServer 8080
```
## 2. 安装ceph-mon ceph-osd ceph-radosgw rpm包

配置机器yum源

vi /etc/yum.repos.d/ceph.repo
```
[ceph]
name=ceph
baseurl=http://127.0.0.1:8080/
enabled=1
gpgcheck=0
```

安装rpm包
```
yum install ceph-mon ceph-osd ceph-radosgw -y
如果出现rpm依赖问题，到网上下载缺少的包到ceph-yum目录后重新createrepo ceph-yum后再次执行安装ceph-mon ceph-osd ceph-radosgw
```

## 3. 安装ceph-deploy

```
pip install ceph-deploy==1.5.39
```

创建ceph-deploy工作目录
```
mkdir onest
cd onest
```

## 4. ceph-deploy节点机器免秘钥登录ceph-mon ceph-osd ceph-radosgw这些节点

```
ssh-keygen
回车回车

ssh-copy-id 主机名字  #事先更新/etc/hosts
```

## 5.初始化配置文件
```
ceph-deploy new 主机名
```

编辑 onest目录下的ceph.conf添加如下

```
[global]
...

osd_crush_chooseleaf_type = 0
osd_pool_default_size = 1
osd_pool_default_min_size = 1
osd_journal_size = 100
osd_max_object_name_len = 460
osd_max_object_namespace_len = 64
```


## 6.初始化mon
```
ceph-deploy mon create-initial

ceph-deploy admin 主机名
结束后ceph -s检查状态
```

## 7.创建osd目录

```
mkdir /var/local/osd0
chmod 777 -R  /var/local/osd0
ceph-deploy --overwrite-conf  osd prepare `hostname -s`:/var/local/osd0
ceph-deploy --overwrite-conf  osd activate `hostname -s`:/var/local/osd0

ceph -s 检查
```

## 8.创建rgw

```
ceph-deploy rgw create 主机名:rgw1
```

## 9.修改rgw配置

vi /etc/ceph/ceph.conf
```
[client.rgw.rgw1]
keyring = /var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring
rgw_frontends = "civetweb port=80"
rgw_enable_ops_log = true
rgw_enable_usage_log = true
```

## 10.重启rgw

```
systemctl restart ceph-radosgw@rgw.rgw1

curl 127.0.0.1

返回

<?xml version="1.0" encoding="UTF-8"?><ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>anonymous</ID><DisplayName></DisplayName></Owner><Buckets></Buckets></ListAllMyBucketsResult>

```

