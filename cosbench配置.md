https://github.com/intel-cloud/cosbench/tree/master/release/conf

# ceph swift
```
<?xml version="1.0" encoding="UTF-8" ?>
<workload name="swift-sample" description="sample benchmark for swift">
<storage type="swift" />
<auth type="swauth" config="username=yuliyang:swift;password=VohZWeiVq2BaB8zbdlSPj1LIrCadaHMysnf4J2vp;auth_url=http://192.168.153.156:7480/auth/v1.0" />
<workflow>
<workstage name="init">
<work type="init" workers="1" config="containers=r(1,32)" />
</workstage>
</workflow>
</workload>
```
