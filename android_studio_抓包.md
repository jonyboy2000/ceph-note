
查看网络

![Imgur](https://i.imgur.com/qHbC3nL.png)

```
cd ~/AppData/Local/Android/Sdk/emulator
$ ./emulator.exe -list-avds
Nexus_5X_API_27
$ ./emulator.exe -avd Nexus_5X_API_27 -http-proxy http://192.168.1.3:8888

```

Fiddler配置

![Imgur](https://i.imgur.com/wpCPTj3.png)

启动虚拟机后打开浏览器，输入
192.168.1.3:8888

![Imgur](https://i.imgur.com/2JyJC3L.png)

点击download the FiddlerRoot certificate

随便输入名字
![Imgur](https://i.imgur.com/jYWGe3I.png) 

网络设置代理

![Imgur](https://i.imgur.com/utEowGF.png)

长按点击Modify network

![Imgur](https://i.imgur.com/94qnMES.png)

填写代理
![Imgur](https://i.imgur.com/NbAJqc8.png)



