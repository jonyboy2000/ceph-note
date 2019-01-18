
```
安装ansible
pip install ansible==2.3.1
//yum install https://cbs.centos.org/kojifiles/packages/ansible/2.3.1.0/1.el7/noarch/ansible-2.3.1.0-1.el7.noarch.rpm  https://cbs.centos.org/kojifiles/packages/ansible/2.3.1.0/1.el7/noarch/ansible-doc-2.3.1.0-1.el7.noarch.rpm  http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-keyczar-0.71c-2.el7.noarch.rpm
yum install sshpass

在ansible机器上执行，设置不校验ssh公钥
export ANSIBLE_HOST_KEY_CHECKING=False


设置主机名
//sudo sed -i 's/^hostname.*/hostname NFJD-PSC-P7F1-S-PM-OS04-ONEST-042/g' /etc/sysconfig/network  解决重启后名字变回来
ansible -i sethost.yml all -m hostname -a "name={{onest_name}}" -u root --ask-pass
mons:
  hosts:
    192.168.1.1:
      onest_name: "web1"
    192.168.1.2:
      onest_name: "web2"
    192.168.1.3:
      onest_name: "web3"

inventory2.yml      
rgws:
  hosts:
    172.16.126.116:
      onest_name: NFJD-PSC-P7F1-S-PM-OS04-ONEST-042
    172.16.126.117:
      onest_name: NFJD-PSC-P7F1-S-PM-OS04-ONEST-043
    172.16.126.118:
      onest_name: NFJD-PSC-P7F1-S-PM-OS04-ONEST-044
      
cat sethost2.yml
---
- hosts: rgws
  become: True
  tasks:
  - name: add myself to /etc/hosts
    lineinfile:
      dest: /etc/sysconfig/network
      regexp: '^hostname[ \t].*'
      line: 'hostname {{onest_name}}'
      state: present

ansible-playbook -i inventory2.yml sethost2.yml -u onest -b --ask-pass

执行下面更新所有机器的系统变量
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

#所有节点安装 libselinux-python
ansible -i inventory.yml all -m shell -a "yum install libselinux-python -y" -u root  --ask-pass

#安装ceph-mon ceph-osd ceph-radosgw ceph-mgr
ansible -i inventory.yml all -m shell -a "yum install ceph-mon ceph-osd ceph-mgr ceph-radosgw http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/lttng-ust-2.4.1-4.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/leveldb-1.12.0-11.el7.x86_64.rpm  http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/l/libbabeltrace-1.2.4-3.el7.x86_64.rpm https://rpmfind.net/linux/epel/7/x86_64/Packages/u/userspace-rcu-0.7.16-1.el7.x86_64.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-pecan-0.4.5-2.el7.noarch.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-simplegeneric-0.8-7.el7.noarch.rpm http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/python-singledispatch-3.4.0.2-2.el7.noarch.rpm https://rpmfind.net/linux/epel/7/x86_64/Packages/f/fcgi-2.4.0-25.el7.x86_64.rpm -y" -u root  --ask-pass


下载ceph-ansile剧本
参考 http://docs.ceph.com/ceph-ansible/stable-3.0/

git clone https://github.com/ceph/ceph-ansible.git
git checkout -b stable-3.0 origin/stable-3.0

编辑配置(grep "^[^#;]"  ceph-ansible/group_vars/all.yml)
vi ceph-ansible/group_vars/all.yml
---
dummy:
ntp_service_enabled: false
ceph_stable: true
ceph_custom: true
ceph_stable_release: jewel           #如果L版本改为 luminous
ceph_origin: distro
public_network: "192.168.130.0/24"   #按实际修改
cluster_network: "192.168.130.0/24"  #按实际修改
monitor_interface: ens34             #mon业务网网卡，按实际修改
journal_size: 10240
osd_mkfs_type: xfs
osd_mkfs_options_xfs: -f -i size=2048 -b size=4096
osd_mount_options_xfs: noatime,largeio,inode64,swalloc
osd_objectstore: filestore   #如果是bluestore 改为 bluestore
devices:
  - '/dev/sdb'
  - '/dev/sdc'
  - '/dev/sdd'
  
osd_scenario: collocated
radosgw_civetweb_port: 7480             #按实际修改
radosgw_civetweb_num_threads: 500       #按实际修改
radosgw_address: "0.0.0.0"
email_address: yuliyang@cmss.chinamobile.com  #按实际修改
ceph_conf_overrides:
  global:
    osd_crush_chooseleaf_type : 0
    osd_pool_default_size : 1     #副本为1，按实际修改
    osd_pool_default_min_size : 1 #最小副本为1，按实际修改
    auth_supported : cephx
    auth_cluster_required : cephx
    auth_service_required : cephx
    auth_client_required : cephx
    osd_pool_default_pg_num : 16   #按实际修改
    osd_pool_default_pgp_num : 16  #按实际修改
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
    rgw_cache_enabled : True
    rgw_cache_lru_size : 100000
    rgw_thread_pool_size : 1000
    rgw_num_rados_handles : 4
    rgw_override_bucket_index_max_shards : 64
    rgw_max_chunk_size : 4194304
    rgw_enable_usage_log : True
    rgw_user_quota_sync_interval : 1800
    rgw_user_quota_sync_wait_time : 1800
    rgw_multipart_min_part_size : 4194304
    rgw_enable_apis : "s3, s3website, swift, swift_auth, admin"
    rgw_bl_work_time : "00:00-24:00"
    rgw_bl_deliver_interval : 3600
    rgw_bl_ops_log_in_hour : true
    rgw_bl_url : "http://127.0.0.1"
    rgw enable static website : true
    rgw_dns_s3website_name : eos-website-guangzhou-1.cmecloud.cn
    rgw_frontends = "civetweb port=80+443s ssl_protocol_version=3 ssl_certificate=/etc/ceph/eos-guangzhou-1.cmecloud.cn.pem"
    rgw_dns_name : eos-guangzhou-1.cmecloud.cn
    public_addr : "{{ ansible_ens32['ipv4']['address'] }}"   #按实际修改 如网卡为eth0 则改ansible_eth0['ipv4']['address']
    cluster_addr : "{{ ansible_ens32['ipv4']['address'] }}"  #按实际修改 如网卡为eth0 则改ansible_eth0['ipv4']['address']
    osd_client_message_size_cap : 1073741824
    osd_client_message_cap : 200
    osd_op_threads : 4
    osd_op_thread_timeout : 60
    osd max scrubs : 1
    osd_scrub_begin_hour : 1
    osd_scrub_end_hour : 5
    osd scrub load threshold : 0.5
    osd scrub min interval : 86400
    osd scrub max interval : 604800
    osd deep scrub interval : 604800
    journal_max_write_entries : 1000
    journal_max_write_bytes : 1073741824
    filestore_op_threads : 4
    filestore_queue_max_ops : 1000
    filestore_queue_max_bytes : 1073741824
    osd_pool_erasure_code_stripe_width : 65535
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

编辑主机表

```
def ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range

mons = ipRange("172.16.126.51", "172.16.126.53")
mons_public = ipRange('172.17.4.51', '172.17.4.53')

osds = ipRange("172.16.126.51", "172.16.126.90")
osds_public = ipRange('172.17.4.51', '172.17.4.90')

rgws = ipRange("172.16.126.118", "172.16.126.122")
rgws_public = ipRange('172.17.4.118', '172.17.4.122')

mgrs = ipRange("172.16.126.51", "172.16.126.53")
mgrs_public = ipRange('172.17.4.51', '172.17.4.53')

resstr =''''''

mons_section = '''mons:
  hosts:
    '''
for mon in mons:
    mons_section += '''%s:
      monitor_interface: bond1
    ''' % (mon,)

osds_section = '''
osds:
  hosts:
    '''
for idx, osd in enumerate(osds):
    osds_section += '''%s:
      public_addr: %s
    ''' % (osd, osds_public[idx])

rgws_section = '''
rgws:
  hosts:
    '''
for idx, rgw in enumerate(rgws):
    rgws_section += '''%s:
    ''' % (rgw,)

mgrs_section = '''
mgrs:
  hosts:
    '''
for idx, mgr in enumerate(mgrs):
    mgrs_section += '''%s:
    ''' % (mgr,)

print resstr + mons_section + osds_section + rgws_section + mgrs_section
```

inventory.yml

```
mons:
  hosts:
    10.144.90.7:
      monitor_interface: enp129s0f0  #按实际修改
    10.144.90.8:
      monitor_interface: enp129s0f0  #按实际修改
    10.144.90.16:
      monitor_interface: enp129s0f0.110@enp129s0f0  #按实际修改
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
        - '/dev/sdd'
rgws:
  hosts:
    192.168.153.183:
    192.168.153.184:

mgrs:
  hosts:
    192.168.153.183:
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

#注释掉，如果部署的是j版本，j版本没有mgr 
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

部署
```
ansible-playbook -i inventory.yml site.yml  -u root --ask-pass
```
等待执行完成
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

卸载集群
```
systemctl reset-failed
#purge
rpm -qa|grep 12.2.5- | awk '{system("yum remove " $1 " -y ")}' && rm -rf /etc/ceph /var/lib/ceph  /var/run/ceph
```


多个rgw实例部署
## multi instance rgw


rgw-standalone-multi.yml
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

```
ansible-playbook -i inventory.yml rgw-standalone-multi.yml  -u root --ask-pass
```

如果配置静态网站执行如下命令
```
ansible -i inventory.yml rgws -m ini_file -a "path=/etc/ceph/ceph.conf section=global option=rgw_enable_static_website value='true' backup=yes"  -u root --ask-pass
ansible -i inventory.yml rgws -m ini_file -a "path=/etc/ceph/ceph.conf section=global option=rgw_dns_s3website_name  value='eos-website.ecloud.com' backup=yes"  -u root --ask-pass
```

