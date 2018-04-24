
```
yum install ppp pptp pptp-setup 

pptpsetup --create vpn --server 10.46.89.192 --username vpn --password vpn --start
modprobe ppp_mppe  
如果报以下错误：
Connect: ppp0 <--> /dev/pts/3  
CHAP authentication succeeded  
LCP terminated by peer (MPPE required but peer refused)  
Modem hangup  

# vm /etc/ppp/peers/vpn  //vpn是上面创建的连接  
文件尾部，加上以下内容  
require-mppe-128  



pppd call vpn
```
