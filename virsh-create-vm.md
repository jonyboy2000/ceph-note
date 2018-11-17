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

```
sed -i 's/Defaults    requiretty/#Defaults    requiretty/g' /etc/sudoers
echo "qemu ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/qemu
chmod 0440 /etc/sudoers.d/qemu
```

# 修改qemu配置

vi /etc/libvirt/qemu.conf

```
user = "qemu"
group = "qemu"
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
      <interface type='network'>
         <mac address='52:54:00:c7:18:b5'/>
         <source network='default'/>
         <model type='virtio'/>
         <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
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
virsh undefine centos  #删除
Domain centos started

virsh list --all
 Id    Name                           State
----------------------------------------------------
 2     centos                         running   #虚拟机 id 此处为2
```

# 下载vnc client
```
https://bintray.com/tigervnc/stable/tigervnc/1.7.0

vnc登录虚拟机后systemctl restart network
```

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
<base64 of client.libvirt.key is output here>
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

nat
```
<?xml version="1.0" encoding="UTF-8"?>
<domain type="kvm">
   <memory unit="GiB">8</memory>
   <vcpu>4</vcpu>
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
         <source file="/tmp/CentOS-7-x86_64-Minimal-1511.iso" />
         <target dev="hda" bus="ide" />
      </disk>
      <disk type="file" device="disk">
         <driver name="qemu" type="raw" />
         <source file="/var/lib/libvirt/images/this_is_os_disk.img" />
         <target dev="vda" bus="virtio" />
      </disk>
      <graphics type="vnc" port="5900" autoport="yes" listen="0.0.0.0" keymap="en-us">
         <listen type="address" address="0.0.0.0" />
      </graphics>
      <video>
         <model type="cirrus" />
         <alias name="video0" />
      </video>
      <interface type='network'>
         <mac address='52:54:00:c7:18:b5'/>
         <source network='default'/>
         <model type='virtio'/>
         <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
      </interface>
   </devices>
   <name>centos</name>
</domain>
```
kvm主机上安装
```
yum -y install spice-server spice-protocol spice-vdagent
```

kvm上的虚拟机安装
```
yum -y install xorg-x11-drv-qxl spice-vdagent
systemctl start spice-vdagentd
systemctl enable spice-vdagentd
```

window7安装
https://releases.pagure.org/virt-viewer/virt-viewer-x64-7.0.msi 

spice://10.254.3.76:5900


```
<?xml version="1.0" encoding="UTF-8"?>
<domain type="kvm">
   <memory unit="GiB">8</memory>
   <vcpu>8</vcpu>
   <os>
      <type arch="x86_64" machine="pc">hvm</type>
      <boot dev="hd" />
      <boot dev="cdrom" />
   </os>
   <features>
      <acpi />
   </features>
   <devices>
      <disk type="file" device="disk">
         <driver name="qemu" type="raw" />
         <source file="/var/lib/libvirt/images/this_is_os_disk.img" />
         <target dev="vda" bus="virtio" />
      </disk>
      <disk type='file' device='disk'>
         <driver name='qemu' type='raw'/>
         <source file='/var/lib/libvirt/images/yehudasa.img'/>
         <target dev='vdb' bus='virtio'/>
      </disk>
      <channel type='spicevmc'>
        <target type='virtio' name='com.redhat.spice.0'/>
        <alias name='channel0'/>
        <address type='virtio-serial' controller='0' bus='0' port='1'/>
      </channel>
      <graphics type='spice' port='5900' autoport='no' listen='0.0.0.0'>
        <listen type='address' address='0.0.0.0'/>
      </graphics>
      <sound model='ac97'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
      </sound>
      <video>
        <model type='qxl' ram='65536' vram='32768' heads='1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
      </video>
      <interface type='network'>
         <mac address='52:84:00:c7:18:b5'/>
         <source network='default'/>
         <model type='virtio'/>
         <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
      </interface>
   </devices>
   <name>ceph76_yly_vm1</name>
</domain>
```



