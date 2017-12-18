#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import json
def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        output = stdout.read()
        ssh.close()
        return output
    except :
        print '%stErrorn'%(ip)

realm_id = ssh2("10.139.13.58","root","jGs*Z+ZQ94TY9T/z",'''radosgw-admin realm  get --rgw-realm=oNest2 |grep id| awk -F '"' '{print $4}' ''').rstrip()
period = ssh2("10.139.13.58","root","jGs*Z+ZQ94TY9T/z",'radosgw-admin period  get --realm-id=%s'%(realm_id,)).rstrip()
period_json = json.loads(period)
period_map = period_json['period_map']
realm_name = period_json['realm_name']

master_zonegroup ={}
slave_zonegroup ={}

for zonegroup in period_map['zonegroups']:
    print zonegroup
    print zonegroup['is_master']
    if zonegroup['is_master'] == 'true':
        master_zonegroup['api_name'] = zonegroup['api_name']
        master_zonegroup['id'] = zonegroup['id']
        master_zonegroup['master_zone'] = zonegroup['master_zone']
    else:
        slave_zonegroup['api_name'] = zonegroup['api_name']
        slave_zonegroup['id'] = zonegroup['id']
        slave_zonegroup['master_zone'] = zonegroup['master_zone']

cmd = "radosgw-admin zonegroup modify --rgw-zonegroup=%s --realm-id=%s --master=false" %(master_zonegroup['api_name'],realm_id,)
ssh2("10.139.13.58","root","jGs*Z+ZQ94TY9T/z",cmd).rstrip()

cmd = "radosgw-admin zonegroup modify --rgw-zonegroup=%s --realm-id=%s --master" %(slave_zonegroup['api_name'],realm_id,)
ssh2("10.139.12.23","root","jGs*Z+ZQ94TY9T/z",cmd).rstrip()

cmd = "radosgw-admin period update --commit --rgw-realm=%s --rgw-zonegroup=%s --rgw-zone=%s" %(realm_name,slave_zonegroup['api_name'],slave_zonegroup['master_zone'],)
ssh2("10.139.12.23","root","jGs*Z+ZQ94TY9T/z",cmd).rstrip()
