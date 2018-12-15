
```
http://xpra.org/

cd /etc/yum.repos.d/
curl -O https://winswitch.org/downloads/CentOS/winswitch.repo
yum install xpra


#启动一个X会话
xpra start :100
#在刚刚启动的会话里运行一个程序，用xterm举例
DISPLAY=:100 xterm
#本地连接这个会话
xpra attach :100
#这时应该就会看到刚刚启动的程序了

#远程可以用ssh
xpra attach ssh:serverhostname:100
```
