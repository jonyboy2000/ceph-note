```
[[local|localrc]]
GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

ADMIN_PASSWORD=stack
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
MYSQL_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=111222333444

HOST_IP=192.168.153.200
SERVICE_HOST=$HOST_IP

OS_PROJECT_NAME=demo
OS_USERNAME=demo
OS_PASSWORD=password
OS_AUTH_URL=http://$SERVICE_HOST:5000/v2.0

DEST=/opt/stack
#RECLONE=yes
PIP_UPGRADE=True
#OFFLINE=True

VERSION=master
NOVNC_BRANCH=v0.6.2
#VERSION=stable/ocata
KEYSTONE_REPO=$GIT_BASE/openstack/keystone.git
KEYSTONE_BRANCH=$VERSION

HORIZON_REPO=$GIT_BASE/openstack/horizon.git
HORIZON_BRANCH=$VERSION

NOVA_REPO=$GIT_BASE/openstack/nova.git
NOVA_BRANCH=$VERSION

NEUTRON_REPO=$GIT_BASE/openstack/neutron.git
NEUTRON_BRANCH=$VERSION

GLANCE_REPO=$GIT_BASE/openstack/glance.git
GLANCE_BRANCH=$VERSION

CINDER_REPO=$GIT_BASE/openstack/cinder.git
CINDER_BRANCH=$VERSION

disable_all_services
enable_service mysql
enable_service rabbit
enable_service key
REGION_NAME=RegionOne

# Disabling Identity API v2
#ENABLE_IDENTITY_V2=False

##### Horizon - Dashboard Service #####
#--------------------------------------
enable_service horizon
enable_service +=,n-api,n-crt,n-obj,n-cpu,n-cond,n-sch,n-novnc,n-cauth,placement-api
disable_service n-net
enable_service neutron
# Neutron options
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta

Q_USE_SECGROUP=True
FLOATING_RANGE=192.168.130.0/24
FIXED_RANGE=10.0.0.0/24
Q_FLOATING_ALLOCATION_POOL=start=192.168.130.201,end=192.168.130.210
PUBLIC_NETWORK_GATEWAY=192.168.130.1
PUBLIC_INTERFACE=ens35
Q_USE_PROVIDERNET_FOR_PUBLIC=True

# Neutron ML2 with OpenvSwitch
Q_PLUGIN=ml2
Q_AGENT=openvswitch
OVS_PHYSICAL_BRIDGE=br-ex
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex

IMAGE_URLS=http://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-uec.tar.gz
enable_service g-api
enable_service g-reg
enable_service +=,cinder,c-api,c-vol,c-sch,c-bak
##### Logging #####
#------------------
LOGFILE=$DEST/logs/stack.sh.log
LOGDIR=$DEST/logs
LOGDAYS=1
LOG_COLOR=False

```
