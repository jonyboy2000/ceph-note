
```
ref http://docs.ceph.com/ceph-ansible/stable-3.0/
pip install ansible==2.3.1
git clone https://github.com/ceph/ceph-ansible.git
git checkout -b stable-3.0 origin/stable-3.0

grep "^[^#;]"  group_vars/all.yml
---
dummy:
ntp_service_enabled: false
ceph_stable: true
ceph_custom: true
ceph_stable_release: luminous
ceph_origin: distro
public_network: "192.168.130.0/24"
cluster_network: "192.168.130.0/24"
monitor_interface: ens34
journal_size: 5120 # OSD journal size in MB
osd_mkfs_type: xfs
osd_mkfs_options_xfs: -f -i size=2048
osd_mount_options_xfs: noatime,largeio,inode64,swalloc
osd_objectstore: filestore
devices:
  - '/dev/sdb'
osd_scenario: collocated
radosgw_interface: ens34
ceph_conf_overrides:
  global:
    osd_crush_chooseleaf_type : 0
    osd_pool_default_size : 1
    osd_pool_default_min_size : 1
```

inventory
```
[mons]
192.168.130.138
[osds]
192.168.130.138
[rgws]
192.168.130.138
[mgrs]
192.168.130.138
```

site.yml
```
---
- hosts:
  - mons
  - osds
  - mgrs  #comment if jewel deploy
  - rgws
  gather_facts: false
  tags:
    - always

  vars:
    delegate_facts_host: True

  tasks:
    # If we can't get python2 installed before any module is used we will fail
    # so just try what we can to get it installed
    - name: check for python2
      stat:
        path: /usr/bin/python
      ignore_errors: yes
      register: systempython2

    - name: install python2 for debian based systems
      raw: sudo apt-get -y install python-simplejson
      ignore_errors: yes
      when:
        - systempython2.stat.exists is undefined or systempython2.stat.exists == false

    - name: gather facts
      setup:
      when:
        - not delegate_facts_host | bool

    - name: gather and delegate facts
      setup:
      delegate_to: "{{ item }}"
      delegate_facts: True
      with_items: "{{ groups['all'] }}"
      run_once: true
      when:
        - delegate_facts_host | bool

- hosts: mons
  gather_facts: false
  become: True
  roles:
    - ceph-defaults
    - ceph-common
    - ceph-config
    - ceph-mon

#comment if jewel deploy
- hosts: mgrs
  gather_facts: false
  become: True
  roles:
    - ceph-defaults
    - ceph-common
    - { role: ceph-config, when: "ceph_release_num.{{ ceph_release }} >= ceph_release_num.luminous" }
    - { role: ceph-mgr, when: "ceph_release_num.{{ ceph_release }} >= ceph_release_num.luminous" }

- hosts: osds
  gather_facts: false
  become: True
  roles:
    - ceph-defaults
    - ceph-common
    - ceph-config
    - ceph-osd

- hosts: rgws
  gather_facts: false
  become: True
  roles:
    - ceph-defaults
    - ceph-common
    - ceph-config
    - ceph-rgw

```

```
ansible-playbook -i inventory site.yml  -u root --ask-pass
```

```
[root@localhost ~]# ceph -s
  cluster:
    id:     208d409f-7119-4c44-be58-446d444c2531
    health: HEALTH_OK

  services:
    mon: 1 daemons, quorum localhost
    mgr: localhost(active)
    osd: 1 osds: 1 up, 1 in
    rgw: 1 daemon active

  data:
    pools:   4 pools, 32 pgs
    objects: 187 objects, 1113 bytes
    usage:   108 MB used, 45948 MB / 46056 MB avail
    pgs:     32 active+clean

```

```
systemctl reset-failed
#purge
rpm -qa|grep 12.2.5- | awk '{system("yum remove " $1 " -y ")}' && rm -rf /etc/ceph /var/lib/ceph  /var/run/ceph
#install
i=10.2.9-25 &&  cmd="yum localinstall ceph-mon-$i.el7.centos.x86_64.rpm ceph-osd-$i.el7.centos.x86_64.rpm ceph-radosgw-$i.el7.centos.x86_64.rpm  ceph-base-$i.el7.centos.x86_64.rpm ceph-common-$i.el7.centos.x86_64.rpm  ceph-selinux-$i.el7.centos.x86_64.rpm  libcephfs1-$i.el7.centos.x86_64.rpm  librados2-$i.el7.centos.x86_64.rpm librbd1-$i.el7.centos.x86_64.rpm  librgw2-$i.el7.centos.x86_64.rpm  libradosstriper1-$i.el7.centos.x86_64.rpm  python-rbd-$i.el7.centos.x86_64.rpm  python-rados-$i.el7.centos.x86_64.rpm  python-cephfs-$i.el7.centos.x86_64.rpm fcgi-2.4.0-25.el7.x86_64.rpm lttng-ust-2.4.1-4.el7.x86_64.rpmleveldb-1.12.0-11.el7.x86_64.rpm libbabeltrace-1.2.4-3.el7.x86_64.rpm userspace-rcu-0.7.16-1.el7.x86_64.rpm" && eval $cmd
```
