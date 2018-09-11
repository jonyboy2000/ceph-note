```
运行cosbench
https://hub.docker.com/r/nexenta/cosbench/

docker pull registry.paas/library/cosbench:latest

单台：
docker run -p 19088:19088 -p 18088:18088 -e ip=业务网ip地址 -e t=both -e n=1 docker.io/nexenta/cosbench:latest

多台：
docker run -p 18088:18088 -e ip=业务网地址 -e t=driver docker.io/nexenta/cosbench:latest

docker run -p 18088:18088 -e ip=业务网地址 -e t=driver docker.io/nexenta/cosbench:latest

docker run -p 19088:19088 -e ip=业务网地址1,业务网地址2 -e t=controller docker.io/nexenta/cosbench:latest

访问controller
http://<controler IP>:19088/controller

```
