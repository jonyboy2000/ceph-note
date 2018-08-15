
```
export ANSIBLE_HOST_KEY_CHECKING=False

/etc/security/limits.conf 更新
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=nofile value=1000000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=nofile value=1000000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=nproc  value=1000000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=nproc  value=1000000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=core value=unlimited" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=core value=unlimited" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=memlock value=32000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=memlock value=32000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=stack value=102400" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=stack value=102400" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=soft limit_item=msgqueue value=8192000" -u root --ask-pass
ansible -i inventory.yml all -m pam_limits -a "domain=* limit_type=hard limit_item=msgqueue value=8192000" -u root --ask-pass
   
ansible -i inventory.yml rgws -m ini_file -a "path=/etc/ceph/ceph.conf section=rgw option=rgw_enable_apis value='s3, s3website, swift, swift_auth, admin' backup=yes"  -u root --ask-pass

ansible -i inventory.yml all -m shell -a "yum install libselinux-python -y" -u root  --ask-pass
ansible -i inventory.yml all -m copy -a "src=10.2.9-25.tar.gz dest=/tmp/" -u root  --ask-pass
ansible -i inventory.yml all -m shell -a "tar xzvfm  /tmp/10.2.9-25.tar.gz -C /tmp/" -u root  --ask-pass
ansible -i inventory.yml all -m shell -a "yum localinstall /tmp/x86_64/ceph-mon-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-osd-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-radosgw-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-base-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-common-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-selinux-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/libcephfs1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librados2-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librbd1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librgw2-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/libradosstriper1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-rbd-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-rados-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-cephfs-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/fcgi-2.4.0-25.el7.x86_64.rpm /tmp/x86_64/lttng-ust-2.4.1-4.el7.x86_64.rpm /tmp/x86_64/leveldb-1.12.0-11.el7.x86_64.rpm /tmp/x86_64/libbabeltrace-1.2.4-3.el7.x86_64.rpm /tmp/x86_64/userspace-rcu-0.7.16-1.el7.x86_64.rpm -y" -u root  --ask-pass

i=10.2.9-25 dir=/tmp/x86_64  && cmd="yum localinstall $dir/ceph-mon-$i.el7.centos.x86_64.rpm  $dir/ceph-osd-$i.el7.centos.x86_64.rpm $dir/ceph-radosgw-$i.el7.centos.x86_64.rpm  $dir/ceph-base-$i.el7.centos.x86_64.rpm $dir/ceph-common-$i.el7.centos.x86_64.rpm  $dir/ceph-selinux-$i.el7.centos.x86_64.rpm  $dir/libcephfs1-$i.el7.centos.x86_64.rpm  $dir/librados2-$i.el7.centos.x86_64.rpm $dir/librbd1-$i.el7.centos.x86_64.rpm  $dir/librgw2-$i.el7.centos.x86_64.rpm $dir/libradosstriper1-$i.el7.centos.x86_64.rpm  $dir/python-rbd-$i.el7.centos.x86_64.rpm  $dir/python-rados-$i.el7.centos.x86_64.rpm  $dir/python-cephfs-$i.el7.centos.x86_64.rpm $dir/fcgi-2.4.0-25.el7.x86_64.rpm $dir/lttng-ust-2.4.1-4.el7.x86_64.rpm $dir/leveldb-1.12.0-11.el7.x86_64.rpm $dir/libbabeltrace-1.2.4-3.el7.x86_64.rpm $dir/userspace-rcu-0.7.16-1.el7.x86_64.rpm -y" && echo $cmd

yum localinstall /tmp/x86_64/ceph-mon-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-osd-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-radosgw-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-base-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-common-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/ceph-selinux-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/libcephfs1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librados2-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librbd1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/librgw2-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/libradosstriper1-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-rbd-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-rados-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/python-cephfs-10.2.9-25.el7.centos.x86_64.rpm /tmp/x86_64/fcgi-2.4.0-25.el7.x86_64.rpm /tmp/x86_64/lttng-ust-2.4.1-4.el7.x86_64.rpm /tmp/x86_64/leveldb-1.12.0-11.el7.x86_64.rpm /tmp/x86_64/libbabeltrace-1.2.4-3.el7.x86_64.rpm /tmp/x86_64/userspace-rcu-0.7.16-1.el7.x86_64.rpm

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
ceph_stable_release: jewel  #luminous
ceph_origin: distro
public_network: "192.168.130.0/24"
cluster_network: "192.168.130.0/24"
monitor_interface: ens34
journal_size: 5120 # OSD journal size in MB
osd_mkfs_type: xfs
osd_mkfs_options_xfs: -f -i size=2048 -b size=4096
osd_mount_options_xfs: noatime,largeio,inode64,swalloc
osd_objectstore: filestore   #bluestore
devices:
  - '/dev/sdb'
osd_scenario: collocated
radosgw_civetweb_port: 8080
radosgw_civetweb_num_threads: 100
radosgw_address: "0.0.0.0"
email_address: yuliyang@cmss.chinamobile.com
ceph_conf_overrides:
  global:
    osd_crush_chooseleaf_type : 0
    osd_pool_default_size : 1
    osd_pool_default_min_size : 1
    auth_supported : cephx
    auth_cluster_required : cephx
    auth_service_required : cephx
    auth_client_required : cephx
    osd_pool_default_pg_num : 16
    osd_pool_default_pgp_num : 16
    debug_tp : 0
    debug_timer : 0
    debug_throttle : 0
    debug_rgw : 0
    debug_rbd : 0
    debug_rados : 0
    debug_perfcounter : 0
    debug_paxos : 0
    debug_osd : 0
    debug_optracker : 0
    debug_objecter : 0
    debug_objectcacher : 0
    debug_objclass : 0
    debug_ms : 0
    debug_monc : 0
    debug_mon : 0
    debug_mds_migrator : 0
    debug_mds_log_expire : 0
    debug_mds_log : 0
    debug_mds_locker : 0
    debug_mds_balancer : 0
    debug_mds : 0
    debug_lockdep : 0
    debug_journaler : 0
    debug_journal : 0
    debug_hadoop : 0
    debug_finisher : 0
    debug_filestore : 0
    debug_filer : 0
    debug_crush : 0
    debug_context : 0
    debug_client : 0
    debug_civetweb : 0
    debug_buffer : 0
    debug_auth : 0
    debug_asok : 0
  rgw:
    rgw_cache_enabled : True
    rgw_cache_lru_size : 100000
    rgw_thread_pool_size : 600
    rgw_num_rados_handles : 4
    rgw_override_bucket_index_max_shards : 64
    rgw_max_chunk_size : 4194304
    rgw_enable_usage_log : True
    rgw_user_quota_sync_interval : 1800
    rgw_user_quota_sync_wait_time : 1800
    rgw_multipart_min_part_size : 4194304
    rgw_enable_apis: "s3, s3website, swift, swift_auth, admin"
  osd:
    public_addr : "{{ ansible_ens32['ipv4']['address'] }}"
    cluster_addr : "{{ ansible_ens32['ipv4']['address'] }}"
    osd_client_message_size_cap : 1073741824
    osd_client_message_cap : 200
    osd_op_threads : 4
    osd_op_thread_timeout : 60
    osd max scrubs : 1
    osd_scrub_begin_hour : 1
    osd_scrub_end_hour : 5
    osd scrub load threshold : 0.5
    osd scrub min interval : 60*60*24
    osd scrub max interval : 60*60*24*7
    osd deep scrub interval : 60*60*24*7
    journal_max_write_entries : 1000
    journal_max_write_bytes : 1073741824
    filestore_op_threads : 4
    filestore_queue_max_ops : 1000
    filestore_queue_max_bytes : 1073741824
    osd_pool_erasure_code_stripe_width : 65535
  mon:
    mon_osd_nearfull_ratio : 0.85
    mon_osd_full_ratio : 0.95
    mon_osd_down_out_interval : 3600
    mon_clock_drift_allowed : 0.15
    osd_pool_default_erasure_code_profile : "plugin=isa technique=reed_sol_van k=4 m=2 ruleset-root=default crush-failure-domain=osd"
os_tuning_params:
  - { name: kernel.pid_max, value: 4194303 }
  - { name: kernel.panic, value: 20 }
  - { name: kernel.hung_task_panic, value: 0 }
  - { name: kernel.hung_task_timeout_secs, value: 120 }
  - { name: kernel.threads-max, value: 1000000 }
  - { name: fs.file-max, value: 26234859 }
  - { name: vm.zone_reclaim_mode, value: 2 }
  - { name: vm.swappiness, value: 60 }
  - { name: vm.min_free_kbytes, value: 4194303 }
  - { name: vm.extra_free_kbytes, value: 4194303 }
```
inventory.yml

```
mons:
  hosts:
    10.144.90.7:
      monitor_interface: enp129s0f0
    10.144.90.8:
      monitor_interface: enp129s0f0
    10.144.90.16:
      monitor_interface: enp129s0f0.110@enp129s0f0
```

```
mons:
  hosts:
    10.144.90.7:
      monitor_interface: enp129s0f0
    10.144.90.8:
      monitor_interface: enp129s0f0
    10.144.90.16:
      monitor_interface: enp129s0f0.110@enp129s0f0
osds:
  hosts:
    192.168.153.183:
      public_addr : 192.168.153.183
      devices:
        - '/dev/sdb'
    192.168.153.184:
      public_addr : 192.168.153.184
      devices:
        - '/dev/sdb'
        - '/dev/sdc'
rgws:
  hosts:
    192.168.153.183:
    192.168.153.184:


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
    - ceph-rgw

```

```
ansible-playbook -i inventory.yml site.yml  -u root --ask-pass
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


## multi instance rgw
rgw-standalone-multi.yml

ansible-playbook -i inventory.yml rgw-standalone-multi.yml  -u root --ask-pass
```
---
- hosts: mons
  become: True
  roles:
    - ceph-defaults
    - ceph-fetch-keys

- hosts: mons
  become: True
  tasks:
  - name: create auth
    command: "{{ item }}"
    with_items:
    - ceph auth get-or-create client.rgw.rgw1  osd 'allow rwx' mon 'allow rw'
    - ceph auth get-or-create client.rgw.rgw2  osd 'allow rwx' mon 'allow rw'
    - ceph auth get-or-create client.rgw.rgw3  osd 'allow rwx' mon 'allow rw'

- hosts: rgws
  become: True
  tasks:
  - name: read cluster fsid if it already exists
    local_action:
      module: command
        cat fetch/ceph_cluster_uuid.conf
    register: cluster_uuid
    become: false
    always_run: true

  - name: set_fact fsid
    set_fact:
      fsid: "{{ cluster_uuid.stdout }}"

  - name: copy admin
    copy:
      src: "fetch/{{ fsid }}{{ item.name }}"
      dest: "{{ item.name }}"
      owner: "ceph"
      group: "ceph"
      mode: "0600"
    with_items:
      - { name: "/etc/ceph/ceph.client.admin.keyring" }

  - name: create dir
    command: "{{ item }}"
    with_items:
    - mkdir -p /var/lib/ceph/radosgw/ceph-rgw.rgw1
    - mkdir -p /var/lib/ceph/radosgw/ceph-rgw.rgw2
    - mkdir -p /var/lib/ceph/radosgw/ceph-rgw.rgw3
    - ceph auth get client.rgw.rgw1 -o /var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring
    - ceph auth get client.rgw.rgw2 -o /var/lib/ceph/radosgw/ceph-rgw.rgw2/keyring
    - ceph auth get client.rgw.rgw3 -o /var/lib/ceph/radosgw/ceph-rgw.rgw3/keyring

  - name: update ceph.conf
    ini_file:
      path: /etc/ceph/ceph.conf
      section: "{{ item.section }}"
      option: "{{ item.option }}"
      value: "{{ item.value }}"
      backup: yes
    with_items:
      - { section: "client.rgw.rgw1", option: "keyring", value: '/var/lib/ceph/radosgw/ceph-rgw.rgw1/keyring' }
      - { section: "client.rgw.rgw1", option: "log file", value: "/var/log/ceph/ceph-rgw-rgw1.log" }
      - { section: "client.rgw.rgw1", option: "rgw frontends", value: "civetweb port=0.0.0.0:8081 num_threads=100" }
      - { section: "client.rgw.rgw2", option: "keyring", value: '/var/lib/ceph/radosgw/ceph-rgw.rgw2/keyring' }
      - { section: "client.rgw.rgw2", option: "log file", value: "/var/log/ceph/ceph-rgw-rgw2.log" }
      - { section: "client.rgw.rgw2", option: "rgw frontends", value: "civetweb port=0.0.0.0:8082 num_threads=100" }
      - { section: "client.rgw.rgw3", option: "keyring", value: '/var/lib/ceph/radosgw/ceph-rgw.rgw3/keyring' }
      - { section: "client.rgw.rgw3", option: "log file", value: "/var/log/ceph/ceph-rgw-rgw3.log" }
      - { section: "client.rgw.rgw3", option: "rgw frontends", value: "civetweb port=0.0.0.0:8083 num_threads=100" }
  - name: enable and start
    command: "{{ item }}"
    with_items:
      - systemctl enable ceph-radosgw@rgw.rgw1
      - systemctl enable ceph-radosgw@rgw.rgw2
      - systemctl enable ceph-radosgw@rgw.rgw3
      - systemctl start ceph-radosgw@rgw.rgw1
      - systemctl start ceph-radosgw@rgw.rgw2
      - systemctl start ceph-radosgw@rgw.rgw3 
```

