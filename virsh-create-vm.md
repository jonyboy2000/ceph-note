# centos7配置KVM
# 检查是否支持虚拟化
```
grep -E '(vmx|svm)' /proc/cpuinfo
```
# 配置转发 
vi /etc/sysctl.conf
```
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 0
net.bridge.bridge-nf-call-iptables = 0
net.bridge.bridge-nf-call-arptables = 0
```

# 生效
```
sysctl -p
```

# 安装rpm包
```
yum install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install virt-viewer bridge-utils
```

# 修改qemu配置

vi /etc/libvirt/qemu.conf

```
user = "root"
group = "root"
dynamic_ownership = 0
```

# 启动
```
systemctl start libvirtd
systemctl enable libvirtd
```
# 检查
```
lsmod | grep kvm
kvm_intel             162153  0
kvm                   525409  1 kvm_intel
```

# 配置网络
```
cd /etc/sysconfig/network-scripts/

vi ifcfg-br0
TYPE=Bridge
BOOTPROTO=dhcp
DEVICE=br0
ONBOOT=yes

vi ifcfg-ens32   #NAT网卡,能连外网
TYPE=Ethernet
DEVICE=ens32
BRIDGE=br0
ONBOOT=yes


2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP qlen 1000
    link/ether 00:0c:29:a2:ca:27 brd ff:ff:ff:ff:ff:ff
13: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether 00:0c:29:a2:ca:27 brd ff:ff:ff:ff:ff:ff
    inet 192.168.100.183/24 brd 192.168.100.255 scope global dynamic br0
       valid_lft 1101sec preferred_lft 1101sec
    inet6 fe80::20c:29ff:fea2:ca27/64 scope link
       valid_lft forever preferred_lft forever
```

# 编辑配置文件 centos7.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<domain type="kvm">
   <memory unit="GiB">4</memory>
   <vcpu>2</vcpu>
   <os>
      <type arch="x86_64" machine="pc">hvm</type>
      <boot dev="hd" />
      <boot dev="cdrom" />
   </os>
   <features>
      <acpi />
   </features>
   <devices>
      <disk type="file" device="cdrom">
         <driver name="qemu" type="raw" />
         <source file="/root/CentOS-7-x86_64-Minimal-1511.iso" />  #镜像
         <target dev="hda" bus="ide" />
      </disk>
      <disk type="file" device="disk">
         <driver name="qemu" type="raw" />
         <source file="/root/this_is_os_disk.img" />
         <target dev="vda" bus="virtio" />
      </disk>
      <graphics type="vnc" port="5900" autoport="yes" listen="0.0.0.0" keymap="en-us">
         <listen type="address" address="0.0.0.0" />
      </graphics>
      <video>
         <model type="cirrus" />
         <alias name="video0" />
      </video>
      <interface type="bridge">
         <mac address="fa:16:3f:68:e3:32" />  #随便一个没使用的
         <source bridge="br0" />
         <model type="virtio" />
         <alias name="net0" />
      </interface>
   </devices>
   <name>centos</name>
</domain>
```

# 创建系统盘
```
qemu-img create this_is_os_disk.img 20G
```

# 从配置文件创建虚拟机
```
virsh create centos7.xml
```

```
virsh list --all
 Id    Name                           State
----------------------------------------------------
 -     centos                         shut off
 
virsh start centos     #启动
virsh shutdown centos  #关机
Domain centos started

virsh list --all
 Id    Name                           State
----------------------------------------------------
 2     centos                         running   #虚拟机 id 此处为2
```

# 下载vnc client
```
https://bintray.com/tigervnc/stable/tigervnc/1.7.0
```

# 查看vmvare 跑KVM的机器的路由
```
route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.100.2   0.0.0.0         UG    425    0        0 br0
192.168.100.0   0.0.0.0         255.255.255.0   U     425    0        0 br0
192.168.122.0   0.0.0.0         255.255.255.0   U     0      0        0 virbr0
192.168.153.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33
```

可以看出 192.168.100.2 为网关


# vnc client连接上虚拟机配置网卡

配置eth0
```
vi /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE=Ethernet
BOOTPROTO=static
IPADDR=192.168.100.200
NETMASK=255.255.255.0
GATEWAY=192.168.100.2  #网关
PEERDNS=yes
PEERROUTES=yes
NAME=eth0
UUID=df95b044-aaa6-4f57-9fb6-3f9ccd201be8
DEVICE=eth0
ONBOOT=yes
```
配置DNS
```
vi /etc/resolv.conf
search localdomain
nameserver 192.168.100.2
```

# 查看是否挂载到br0网桥下
```
brctl show
bridge name	 bridge id	      	STP enabled	interfaces
br0		 8000.000c29a2ca27	no		ens32        #bridge
						        net0
virbr0		 8000.525400a8ceff	yes		virbr0-nic   #NAT
```
本机ssh root@192.168.100.200 就可以了


# 添加硬盘

```

qemu-img create data.img 10G

vi disk.xml

<disk type='file' device='disk'>
	<driver name='qemu' type='raw'/>
	<source file='/root/data.img'/>
	<target dev='vdb' bus='virtio'/>
</disk>

virsh attach-device 2 disk.xml
```


# 添加网卡
```
vi network.xml
<interface type="bridge">
         <mac address="fa:17:3f:6s:e3:33" />
         <source bridge="br0" />
         <model type="virtio" />
         <alias name="net1" />
</interface>

virsh attach-device 2 network.xml
```

# 删除设备
```
virsh detach-device 2 disk.xml
virsh detach-device 2 network.xml
```

# 删除虚拟机
```
virsh destroy 2
```

# 参考博客
https://www.linuxtechi.com/install-kvm-hypervisor-on-centos-7-and-rhel-7

http://www.hanbaoying.com/2017/09/19/virsh-create-vm.html


# rbd

## vstart 启动测试集群
```
yum install ceph-mon ceph-osd
#vstart.sh脚本参考https://github.com/wzyuliyang/ceph-note/blob/master/ceph-dev/debug_rgw.md
CEPH_BUILD_ROOT=/usr CEPH_PORT=6789 ./vstart.sh -n --mon_num 1 --mds_num 0  --short -r -X -i 192.168.100.186
```

## 创建存储池
```
ceph osd pool create libvirt-pool 128 128
```
## 创建key
```
ceph auth get-or-create client.libvirt mon 'allow r' osd 'allow class-read object_prefix rbd_children, allow rwx pool=libvirt-pool'
```

## 创建 secret.xml
```
cat > secret.xml <<EOF
<secret ephemeral='no' private='no'>
        <usage type='ceph'>
                <name>client.libvirt secret</name>
        </usage>
</secret>
EOF

virsh secret-define --file secret.xml
<uuid of secret is output here>
```

## ceph机器上获取ceph auth key
```
ceph auth get-key client.libvirt | sudo tee client.libvirt.key
<base64 of client.libvirt.key>
```

## KVM机器上设置libvirt用到的ceph auth key
```
virsh secret-set-value --secret {uuid of secret} --base64 {base64 of client.libvirt.key}
```

## 创建镜像

 

```
#kvm机器上获取ceph.conf
scp 192.168.100.186:/root/ceph1/ceph.conf /etc/ceph/
#创建
qemu-img create -f rbd rbd:libvirt-pool/new-libvirt-image 2G
```

vi rbddisk.xml
```
<disk type='network' device='disk'>
        <source protocol='rbd' name='libvirt-pool/new-libvirt-image'>
                    <host name='192.168.100.186' port='6789'/>
        </source>
        <auth username='libvirt'>
            <secret type='ceph' uuid='uuid of secret'/>
        </auth>
        <target dev='vdc' bus='virtio'/>
</disk>
```
挂载
```
virsh attach-device centos rbddisk.xml
```

