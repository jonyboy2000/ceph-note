|  IP  	| 192.168.153.148 	| 192.168.153.149 	| 192.168.153.150 	|
|:----:	|:---------------:	|:---------------:	|:---------------:	|
| ROLE 	|    CONTROLLER   	|      VOLUME     	|     COMPUTE     	|

# base
[controller/volume]
```
yum install python-openstackclient openstack-selinux -y

```
[controller]
```
yum install rabbitmq-server -y
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
rabbitmqctl add_user openstack openstack
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
yum install memcached python-memcached -y
systemctl enable memcached.service
systemctl start memcached.service
rabbitmq-plugins enable rabbitmq_management
```

keystone,glance,nova,neutron[controller]
```
yum install openstack-keystone httpd mod_wsgi -y
yum install openstack-glance -y
yum install openstack-nova-api openstack-nova-conductor  openstack-nova-console openstack-nova-novncproxy openstack-nova-scheduler -y
yum install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge ebtables -y
```

数据库[controller]
```
yum install mariadb mariadb-server python2-PyMySQL -y
vi /etc/my.cnf.d/openstack.cnf
[mysqld]
bind-address = 192.168.153.148
default-storage-engine = innodb
innodb_file_per_table
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8

systemctl enable mariadb.service
systemctl start mariadb.service
mysql_secure_installation

create database keystone;
grant all on keystone.* to 'keystone'@'localhost' identified by 'keystone';
grant all on keystone.* to 'keystone'@'%' identified by 'keystone';
create database glance;
grant all on glance.* to 'glance'@'localhost' identified by 'glance';
grant all on glance.* to 'glance'@'%' identified by 'glance';
create database nova;
grant all on nova.* to 'nova'@'localhost' identified by 'nova';
grant all on nova.* to 'nova'@'%' identified by 'nova';
create database nova_api;
grant all on nova_api.* to 'nova'@'localhost' identified by 'nova';
grant all on nova_api.* to 'nova'@'%' identified by 'nova';
create database neutron;
grant all on neutron.* to 'neutron'@'localhost' identified by 'neutron';
grant all on neutron.* to 'neutron'@'%' identified by 'neutron';
create database cinder;
grant all on cinder.* to 'cinder'@'localhost' identified by 'cinder';
grant all on cinder.* to 'cinder'@'%' identified by 'cinder';
```

[compute]
```
yum install openstack-nova-compute -y
yum install openstack-neutron-linuxbridge ebtables ipset -y
```

[controller配置keystone]
```
/etc/keystone/keystone.conf
[database]
connection = mysql+pymysql://keystone:keystone@192.168.153.148/keystone
[token]
provider = fernet

su -s /bin/sh -c "keystone-manage db_sync" keystone
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
keystone-manage bootstrap --bootstrap-password admin --bootstrap-admin-url http://192.168.153.148:35357/v3/ --bootstrap-internal-url http://192.168.153.148:35357/v3/ --bootstrap-public-url http://192.168.153.148:5000/v3/ --bootstrap-region-id RegionOne

/etc/httpd/conf/httpd.conf
ServerName 192.168.153.148

ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

systemctl enable httpd.service
systemctl start httpd.service

export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_DOMAIN_NAME=default
export OS_AUTH_URL=http://192.168.153.148:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
```
```
openstack project create --domain default --description "Service Project" service

openstack project create --domain default --description "Demo Project" demo

openstack user create --domain default --password-prompt demo
openstack role create user
openstack role add --project demo --user demo user
```

[controller配置glance]
```
openstack user create --domain default --password-prompt glance
openstack role add --project service --user glance admin
openstack service create --name glance --description "OpenStack Image" image

openstack endpoint create --region RegionOne image public http://192.168.153.148:9292

openstack endpoint create --region RegionOne image internal http://192.168.153.148:9292

openstack endpoint create --region RegionOne image admin http://192.168.153.148:9292

/etc/glance/glance-api.conf
[database]
connection = mysql+pymysql://glance:glance@192.168.153.148/glance
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = glance

[paste_deploy]
flavor = keystone

[glance_store]
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/


/etc/glance/glance-registry.conf

[database]
connection = mysql+pymysql://glance:glance@192.168.153.148/glance
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = glance
[paste_deploy]
flavor = keystone


su -s /bin/sh -c "glance-manage db_sync" glance

systemctl enable openstack-glance-api.service openstack-glance-registry.service
systemctl start openstack-glance-api.service openstack-glance-registry.service


openstack image create "cirros"  --file cirros-0.3.4-x86_64-disk.img  --disk-format qcow2 --container-format bare  --public

openstack image list
```
[controller配置nova]
```
openstack user create --domain default --password-prompt nova
openstack role add --project service --user nova admin
openstack service create --name nova --description "OpenStack Compute" compute

openstack endpoint create --region RegionOne compute public http://192.168.153.148:8774/v2.1/%\(tenant_id\)s

openstack endpoint create --region RegionOne compute internal http://192.168.153.148:8774/v2.1/%\(tenant_id\)s

openstack endpoint create --region RegionOne compute admin http://192.168.153.148:8774/v2.1/%\(tenant_id\)s


/etc/nova/nova.conf

[DEFAULT]
enabled_apis = osapi_compute,metadata
transport_url=rabbit://openstack:openstack@192.168.153.148
auth_strategy = keystone
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
[api_database]
connection=mysql+pymysql://nova:nova@192.168.153.148/nova_api
[database]
connection=mysql+pymysql://nova:nova@192.168.153.148/nova
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = nova
[vnc]
vncserver_listen = 192.168.153.148
vncserver_proxyclient_address = 192.168.153.148
[glance]
api_servers = http://192.168.153.148:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp


su -s /bin/sh -c "nova-manage api_db sync" nova
su -s /bin/sh -c "nova-manage db sync" nova

systemctl enable openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service


systemctl start openstack-nova-api.service openstack-nova-consoleauth.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service

```

[compute]
```
/etc/nova/nova.conf
[DEFAULT]
enabled_apis = osapi_compute,metadata
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@192.168.153.148
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = nova
[vnc]
enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = 192.168.153.150
novncproxy_base_url = http://192.168.153.148:6080/vnc_auto.html
[glance]
api_servers = http://192.168.153.148:9292
[oslo_concurrency]
lock_path = /var/lib/nova/tmp
virt_type=qemu


systemctl enable libvirtd.service openstack-nova-compute.service
systemctl start libvirtd.service openstack-nova-compute.service
```

[controller] neutron
```
[root@controller ~]# nova service-list
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| Id | Binary           | Host       | Zone     | Status  | State | Updated_at                 | Disabled Reason |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| 1  | nova-consoleauth | controller | internal | enabled | up    | 2017-01-23T03:07:58.000000 | -               |
| 2  | nova-conductor   | controller | internal | enabled | up    | 2017-01-23T03:07:58.000000 | -               |
| 3  | nova-scheduler   | controller | internal | enabled | up    | 2017-01-23T03:07:58.000000 | -               |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
[root@controller ~]# nova service-list
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| Id | Binary           | Host       | Zone     | Status  | State | Updated_at                 | Disabled Reason |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+
| 1  | nova-consoleauth | controller | internal | enabled | up    | 2017-01-23T03:10:08.000000 | -               |
| 2  | nova-conductor   | controller | internal | enabled | up    | 2017-01-23T03:10:08.000000 | -               |
| 3  | nova-scheduler   | controller | internal | enabled | up    | 2017-01-23T03:10:08.000000 | -               |
| 6  | nova-compute     | compute    | nova     | enabled | up    | 2017-01-23T03:10:05.000000 | -               |
+----+------------------+------------+----------+---------+-------+----------------------------+-----------------+


openstack image list

openstack user create --domain default --password-prompt neutron
openstack role add --project service --user neutron admin
openstack service create --name neutron --description "OpenStack Networking" network

openstack endpoint create --region RegionOne network public http://192.168.153.148:9696

openstack endpoint create --region RegionOne network internal http://192.168.153.148:9696

openstack endpoint create --region RegionOne network admin http://192.168.153.148:9696 


/etc/neutron/neutron.conf

[database]
connection = mysql+pymysql://neutron:neutron@192.168.153.148/neutron

[DEFAULT]
core_plugin = ml2
notify_nova_on_port_status_changes = True
notify_nova_on_port_data_changes = True
auth_strategy = keystone
service_plugins =
transport_url = rabbit://openstack:openstack@192.168.153.148

[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = neutron

[nova]
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = nova
password = nova

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp


/etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
type_drivers = flat,vlan,gre,vxlan,geneve
tenant_network_types =
mechanism_drivers = linuxbridge
extension_drivers = port_security
[ml2_type_flat]
flat_networks = public
[securitygroup]
enable_ipset = True

/etc/neutron/plugins/ml2/linuxbridge_agent.ini

[linux_bridge]
physical_interface_mappings = public:eth0
physical_interface_mappings = public:bond4_1.1003  
[vxlan]
enable_vxlan = False
[securitygroup]
enable_security_group = True
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

/etc/neutron/dhcp_agent.ini
[DEFAULT]
interface_driver = neutron.agent.linux.interface.BridgeInterfaceDriver
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = True

/etc/neutron/metadata_agent.ini
[DEFAULT]
nova_metadata_ip = 192.168.153.148
metadata_proxy_shared_secret = trying

/etc/nova/nova.conf
[neutron]
url = http://192.168.153.148:9696
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = True
metadata_proxy_shared_secret = trying

ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini

su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

systemctl restart openstack-nova-api.service

systemctl enable neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service
```

[compute]
```
/etc/neutron/neutron.conf
[DEFAULT]
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@192.168.153.148


[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = neutron

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp


/etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = public:ens34
[vxlan]
enable_vxlan = False
[securitygroup]
enable_security_group = True
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

/etc/nova/nova.conf
[neutron]
url = http://192.168.153.148:9696
auth_url = http://192.168.153.148:35357
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = neutron
password = neutron

systemctl restart openstack-nova-compute.service
systemctl enable neutron-linuxbridge-agent.service
systemctl start neutron-linuxbridge-agent.service
```

[controller]
```
neutron ext-list
neutron agent-list
[root@controller ~]# neutron agent-list
+--------------------------------------+--------------------+------------+-------------------+-------+----------------+---------------------------+
| id                                   | agent_type         | host       | availability_zone | alive | admin_state_up | binary                    |
+--------------------------------------+--------------------+------------+-------------------+-------+----------------+---------------------------+
| 1fffc77c-6958-4ac9-8d0a-658c3b7f6e72 | Linux bridge agent | controller |                   | :-)   | True           | neutron-linuxbridge-agent |
| 21937a98-4426-4a4f-b2ae-86bd6ea5358a | Linux bridge agent | compute    |                   | :-)   | True           | neutron-linuxbridge-agent |
| 282ee8f9-ed26-4f99-8768-6571e1930b72 | DHCP agent         | controller | nova              | :-)   | True           | neutron-dhcp-agent        |
| eda1f87a-4095-4d05-9559-e1c3932da28a | Metadata agent     | controller |                   | :-)   | True           | neutron-metadata-agent    |
+--------------------------------------+--------------------+------------+-------------------+-------+----------------+---------------------------+

```

[compute]
```
openstack network create --share --provider-physical-network public --provider-network-type flat public

openstack subnet create --network public --allocation-pool start=192.168.150.200,end=192.168.150.230 --dns-nameserver 192.168.150.2 --gateway 192.168.150.2 --subnet-range 192.168.0.0/16 public-instance
```
[controller]
```
openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano
openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey
openstack keypair list
openstack security group rule create --proto icmp default
openstack security group rule create --proto tcp --dst-port 22 default
[root@controller ~]# openstack flavor list
+----+---------+-----+------+-----------+-------+-----------+
| ID | Name    | RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+---------+-----+------+-----------+-------+-----------+
| 0  | m1.nano |  64 |    1 |         0 |     1 | True      |
+----+---------+-----+------+-----------+-------+-----------+
[root@controller ~]# openstack network list
+--------------------------------------+--------+--------------------------------------+
| ID                                   | Name   | Subnets                              |
+--------------------------------------+--------+--------------------------------------+
| 3d536cb7-5a58-452f-a461-f12fd3129e52 | public | 3cb136e9-0315-4cd5-8be0-a7049d146732 |
+--------------------------------------+--------+--------------------------------------+
[root@controller ~]# openstack image list
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| d1ee6656-353e-42d8-8756-c5ed98fd7f02 | cirros | active |
+--------------------------------------+--------+--------+
[root@controller ~]#  openstack security group list
+--------------------------------------+---------+-------------+----------------------------------+
| ID                                   | Name    | Description | Project                          |
+--------------------------------------+---------+-------------+----------------------------------+
| a02d525b-9809-40ba-aeac-31cc067ba861 | default | 缺省安全组  | bb63988618664e3099be225e8b8fd485 |
+--------------------------------------+---------+-------------+----------------------------------+

openstack server create --flavor m1.nano --image cirros --nic net-id=3d536cb7-5a58-452f-a461-f12fd3129e52 --security-group default --key-name mykey public-instance

[root@controller ~]# openstack server list
+--------------------------------------+-----------------+--------+------------------------+------------+
| ID                                   | Name            | Status | Networks               | Image Name |
+--------------------------------------+-----------------+--------+------------------------+------------+
| a80a746c-8619-4118-ab40-0f09cd907850 | public-instance | ACTIVE | public=192.168.150.208 | cirros     |
+--------------------------------------+-----------------+--------+------------------------+------------+
ssh cirros@192.168.150.208
user:cirros
password:cubswin:)

openstack console url show public-instance 
```
[controller]
```
openstack user create --domain default --password-prompt cinder
openstack role add --project service --user cinder admin
openstack service create --name cinder --description "OpenStack Block Storage" volume
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
openstack endpoint create --region RegionOne   volume admin http://192.168.153.148:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volume internal http://192.168.153.148:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volume public http://192.168.153.148:8776/v1/%\(tenant_id\)s

openstack endpoint create --region RegionOne   volumev2 public http://192.168.153.148:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volumev2 internal http://192.168.153.148:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne   volumev2 admin http://192.168.153.148:8776/v2/%\(tenant_id\)s

yum install openstack-cinder -y
vi /etc/cinder/cinder.conf
[database]
connection = mysql+pymysql://cinder:cinder@192.168.153.148/cinder 
[DEFAULT]
transport_url = rabbit://openstack:openstack@192.168.153.148
auth_strategy = keystone
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = cinder
[oslo_concurrency]
lock_path = /var/lib/cinder/tmp


iscsi_ip_address = 192.168.153.148

su -s /bin/sh -c "cinder-manage db sync" cinder


/etc/nova/nova.conf
[cinder]
os_region_name = RegionOne

systemctl restart openstack-nova-api.service
systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service
systemctl start openstack-cinder-api.service openstack-cinder-scheduler.service
[root@controller ~]# cinder service-list
+------------------+------------+------+---------+-------+----------------------------+-----------------+
| Binary           | Host       | Zone | Status  | State | Updated_at                 | Disabled Reason |
+------------------+------------+------+---------+-------+----------------------------+-----------------+
| cinder-scheduler | controller | nova | enabled | up    | 2017-01-23T06:34:56.000000 | -               |
+------------------+------------+------+---------+-------+----------------------------+-----------------+

```

[compute]
```
/etc/nova/nova.conf
[cinder]
os_region_name = RegionOne
```

[volume]
```
yum install lvm2
systemctl enable lvm2-lvmetad.service
systemctl start lvm2-lvmetad.service


[root@volume ~]# lsblk -f
NAME                         FSTYPE      LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1                       ext4              d0f7f2b7-d7f6-47b8-81ee-e7365711a4ba   /boot
└─sda2                       LVM2_member       qYShvG-Xirl-wLST-j0gU-iXPk-34Qx-15mSKA
  ├─bclinux-root             ext4              4e448946-20a4-40c4-a9c6-7f5c12d94bc2   /
  ├─bclinux-swap             swap              ef5c4b36-c315-43ff-a9d4-ff0fe796bf8f   [SWAP]
  └─bclinux-docker--poolmeta
sdb

/etc/lvm/lvm.conf 修改filter
[root@volume ~]# pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created

[root@volume ~]# vgcreate cinder-volumes /dev/sdb
  Volume group "cinder-volumes" successfully created

如果出现 pvcreate /dev/sdb Device /dev/sdb not found (or ignored by filtering).
[onest@ceph04 yuliyang]$ sudo dd if=/dev/urandom of=/dev/sdb bs=512 count=64
64+0 records in
64+0 records out
32768 bytes (33 kB) copied, 0.0034822 s, 9.4 MB/s
[onest@ceph04 yuliyang]$ sudo pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created
  
  
  
yum install openstack-cinder targetcli python-keystone -y

/etc/cinder/cinder.conf
[DEFAULT]
glance_api_servers = http://192.168.153.148:9292
auth_strategy = keystone
enabled_backends = lvm
transport_url = rabbit://openstack:openstack@192.168.153.148
[oslo_concurrency]
lock_path = /var/lib/cinder/tmp
[database]
connection = mysql+pymysql://cinder:cinder@192.168.153.148/cinder
[keystone_authtoken]
auth_uri = http://192.168.153.148:5000
auth_url = http://192.168.153.148:35357
memcached_servers = 192.168.153.148:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = cinder



iscsi_ip_address = 192.168.153.149
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = lioadm


systemctl enable openstack-cinder-volume.service target.service
systemctl start openstack-cinder-volume.service target.service
```

[controller]
```
[root@controller ~]# openstack volume service list
+------------------+------------+------+---------+-------+----------------------------+
| Binary           | Host       | Zone | Status  | State | Updated At                 |
+------------------+------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller | nova | enabled | up    | 2017-01-23T06:46:18.000000 |
+------------------+------------+------+---------+-------+----------------------------+
[root@controller ~]# openstack volume service list
+------------------+------------+------+---------+-------+----------------------------+
| Binary           | Host       | Zone | Status  | State | Updated At                 |
+------------------+------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller | nova | enabled | up    | 2017-01-23T06:48:38.000000 |
| cinder-volume    | volume@lvm | nova | enabled | up    | 2017-01-23T06:48:43.000000 |
+------------------+------------+------+---------+-------+----------------------------+

#1G
openstack volume create --size 1 volume1
[root@controller ~]# openstack volume list
+--------------------------------------+--------------+-----------+------+-------------+
| ID                                   | Display Name | Status    | Size | Attached to |
+--------------------------------------+--------------+-----------+------+-------------+
| eac8b89c-ca5a-47af-89d0-a9917e1ec11d | volume1      | available |    1 |             |
+--------------------------------------+--------------+-----------+------+-------------+

openstack server add volume public-instance volume1
[root@controller ~]# ssh cirros@192.168.150.208
$ lsblk -f
NAME   FSTYPE LABEL MOUNTPOINT
vda
`-vda1              /
vdb


[root@controller ~]# openstack volume list
+--------------------------------------+--------------+--------+------+------------------------------------------+
| ID                                   | Display Name | Status | Size | Attached to                              |
+--------------------------------------+--------------+--------+------+------------------------------------------+
| eac8b89c-ca5a-47af-89d0-a9917e1ec11d | volume1      | in-use |    1 | Attached to public-instance on /dev/vdb  |
+--------------------------------------+--------------+--------+------+------------------------------------------+
[root@controller ~]# openstack server remove volume public-instance volume1
[root@controller ~]# openstack volume list
+--------------------------------------+--------------+-----------+------+-------------+
| ID                                   | Display Name | Status    | Size | Attached to |
+--------------------------------------+--------------+-----------+------+-------------+
| eac8b89c-ca5a-47af-89d0-a9917e1ec11d | volume1      | available |    1 |             |
+--------------------------------------+--------------+-----------+------+-------------+
[root@controller ~]# ssh cirros@192.168.150.208
$ lsblk -f
NAME   FSTYPE LABEL MOUNTPOINT
vda
`-vda1              /

```

[volume]
```
systemctl enable openstack-cinder-backup.service
systemctl start openstack-cinder-backup.service
```

[controller]
```
/etc/cinder/cinder.conf
backup_swift_url = http://10.128.3.68/swift/v1
openstack volume list
openstack server remove volume public-instance volume1
cinder help backup-create
cinder backup-create  ef3a93f7-c57b-4834-9f0e-6482fa9e1296  
cinder backup-create  ef3a93f7-c57b-4834-9f0e-6482fa9e1296  --incremental True
创建一个全量备份：
cinder backup-create [--display-name <display-name>] <volume>
创建一个增量备份：
cinder backup-create [--display-name <display-name>] --incremental True <volume>

[onest@ceph04 yuliyang]$ cinder backup-list
+--------------------------------------+--------------------------------------+----------+------+------+--------------+---------------+
| ID                                   | Volume ID                            | Status   | Name | Size | Object Count | Container     |
+--------------------------------------+--------------------------------------+----------+------+------+--------------+---------------+
| 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 | ef3a93f7-c57b-4834-9f0e-6482fa9e1296 | creating | -    | 1    | 0            | volumebackups |
+--------------------------------------+--------------------------------------+----------+------+------+--------------+---------------+
[onest@ceph04 yuliyang]$ cinder backup-delete 461b51c1-7c9e-4c41-9f03-23cba4c0ef23
Delete for backup 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 failed: Invalid backup: Backup status must be available or error (HTTP 400) (Request-ID: req-c56b117a-d5fb-444e-8c7e-80945ebd98ed)
ERROR: Unable to delete any of the specified backups.
[onest@ceph04 yuliyang]$ cinder backup-list
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| ID                                   | Volume ID                            | Status    | Name | Size | Object Count | Container     |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 | ef3a93f7-c57b-4834-9f0e-6482fa9e1296 | available | -    | 1    | 22           | volumebackups |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+

```

