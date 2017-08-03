```
./cosbench.sh

for i in `seq -w 01 05`;do ssh  ceph$i  sh -c "sync && echo 3 |  tee /proc/sys/vm/drop_caches";done

./cli.sh submit cosbench-20.xml
```
