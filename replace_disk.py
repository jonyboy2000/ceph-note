#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import json, time

def getuuid(jsoncontent, osdid):
    try:
        json_object = json.loads(jsoncontent)
    except ValueError, e:
        print "json error"
        return None
    for osd in json_object['osds']:
        if str(osd['osd']) == str(osdid.rstrip()):
            return osd['uuid']
    return None


disk = raw_input("请输入磁盘设备[sdb]\n")

try:
    cmd = 'lsblk -f |grep %s| grep ceph ' % (disk,)
    results = subprocess.check_output(cmd, shell=True)
    print(results)
except:
    print "lsblk -f error"

osdid = None
try:
    cmd = "lsblk -f |grep %s| grep ceph |awk '{print $4}' |cut -c 24- " % (disk,)
    osdid = subprocess.check_output(cmd, shell=True)
except:
    print "get osd id error"

jsondump = None
try:
    cmd = "ceph osd dump --format json"
    jsondump = subprocess.check_output(cmd, shell=True)
except:
    print "get osd id error"

uuid = getuuid(jsondump, osdid)

mountpoint = None
try:
    cmd = "lsblk -f |grep %s| grep ceph |awk '{print $4}'" % (disk,)
    mountpoint = subprocess.check_output(cmd, shell=True)
except:
    print "get mount point error"

try:
    cmd = "sudo systemctl stop ceph-osd@%s" % (osdid,)
    print cmd
    stoposd = subprocess.check_output(cmd, shell=True)
except:
    print "stop osd error"

time.sleep(5)

try:
    cmd = "umount %s" % (mountpoint,)
    mountpoint = subprocess.check_output(cmd, shell=True)
except:
    print "umount error"

try:
    cmd = "ceph auth del osd.%s" % (osdid,)
    mountpoint = subprocess.check_output(cmd, shell=True)
except:
    print "auth del error"

insertcomfire = 'no'
while insertcomfire != 'yes':
    insertcomfire = raw_input("确认已经插入新盘[yes or no]\n")
    if insertcomfire == 'yes':
        newdisk = raw_input("新盘[sdb ? sdc ? or]\n")
        try:
            cmd = 'lsblk -f |grep %s ' % (newdisk,)
            results = subprocess.check_output(cmd, shell=True)
            if results:
                try:
                    cmd = "ceph-disk prepare --zap-disk /dev/%s --osd-uuid %s" % (newdisk, uuid)
                    prepareresult = subprocess.check_output(cmd, shell=True)
                except:
                    print "prepare osd error"
        except:
            print "not found"
            insertcomfire = 'no'
