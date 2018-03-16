
macos 10.13

https://stackoverflow.com/questions/46593880/xdebug-on-macos-10-13-with-php-7

```
sudo vi /etc/php.ini

proxychains4 git clone git://github.com/xdebug/xdebug.git
cd xdeug
phpize
./configure
make
sudo cp modules/xdebug.so /usr/lib/php/extensions/



[xdebug]
zend_extension = "/Users/yuliyang/xdebug/modules/xdebug.so"
xdebug.remote_enable=1
xdebug.remote_log="/Users/yuliyang/xdebug/modules/xdebug.log"
xdebug.remote_host="127.0.0.1"
xdebug.remote_handler="dbgp"
xdebug.remote_mode="req"
xdebug.remote_port=9001

```

[Imgur](https://i.imgur.com/ZogfCoq.png)

[Imgur](https://i.imgur.com/ScN1arq.png)

[Imgur](https://i.imgur.com/3tEp4Ab.png)

访问 http://localhost:8080/info.php  [不要访问 http://127.0.0.1:8080/info.php]

[Imgur](https://i.imgur.com/xfg694M.png)


