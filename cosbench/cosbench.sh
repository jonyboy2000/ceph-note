#!/bin/sh
container="cosbenchyly"
for i in `seq 1 20`;do
cat > cosbench-$i.xml << EOF
<?xml version="1.0" encoding="UTF-8" ?>
<workload name="docker0-put data to $container$i 100 Workers 64k" description="sample benchmark for s3 dns">
<workflow>
<workstage name="docker0-put data to $container$i 100 Workers 64k">
       <work name="Put64KBData" workers="100"  totalOps="10000" driver="driver1">
       	 <storage type="s3" config="accesskey=cosbench;secretkey=cosbench;endpoint=http://10.147.5.92:8083/;path_style_access=true" />
         <operation type="write" ratio="100" config="cprefix=$container;oprefix=data-$i-100wks_64k;containers=c($i);objects=s(1,10000);sizes=c(64)KB" />
       </work>
    </workstage>
</workflow>
</workload>
EOF
done
