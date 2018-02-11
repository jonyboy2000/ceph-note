
```
yum install  ftp://ftp.pbone.net/mirror/rpmfusion.org/free/el/updates/7/x86_64/l/librtmp-2.4-7.20160224.gitfa8646d.el7.x86_64.rpm https://www.rpmfind.net/linux/rpmfusion/free/el/updates/7/x86_64/l/librtmp-devel-2.4-7.20160224.gitfa8646d.el7.x86_64.rpm
git clone https://github.com/sqbing/infinite_push_rtmp.git
g++  main.cc -l rtmp -o infinite_push
./infinite_push -i ~/whatever.flv -o rtmp://xxx.xxx.xxx.xxx/live/test
```
