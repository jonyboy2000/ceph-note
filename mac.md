brew curl
```
~/.curlrc
socks5 = "localhost:1080"
```

g++7.2安装
```
https://github.com/sol-prog/gcc-osx-binary
```
boost 安装
下载解压源码
```
./bootstrap.sh --prefix=/usr/local/boost-1.60.0
```
vim  project-config.jam
```
#if ! darwin in [ feature.values <toolset> ]
#{
#    using darwin ; 
#}
 
#project : default-build <toolset>darwin ;
```

```
#project : default-build <toolset>darwin ;
using gcc : 7.2 : g++-7.2 ;
```

```
sudo ./b2 cxxflags=-std=c++14 install
```

https://solarianprogrammer.com/2016/03/06/compiling-boost-gcc-5-clang-mac-os-x/

cmakelists.txt配置
```
cmake_minimum_required(VERSION 3.9)
project(untitled2)
set(CMAKE_CXX_STANDARD 11)
set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
set(Boost_INCLUDE_DIR /usr/local/boost-1.60.0/include/)
set(Boost_LIBRARY_DIR /usr/local/boost-1.60.0/lib/)
find_package(Boost COMPONENTS system filesystem regex REQUIRED)
include_directories(${Boost_INCLUDE_DIR})
add_executable(untitled2 main.cpp)
target_link_libraries(untitled2 ${Boost_LIBRARIES})
```


nginx
```
wget:
nginx: http://nginx.org/download/nginx-1.12.2.tar.gz
zlib: http://zlib.net/zlib-1.2.11.tar.gz
pcre: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.gz
openssl: https://www.openssl.org/source/openssl-1.1.0g.tar.gz

cd nginx* && mkdir build

./configure --prefix=/Users/yuliyang/Downloads/nginx/build --with-cc=gcc-7.2 --with-debug --with-zlib=../zlib-1.2.11 --with-pcre=../pcre-8.38 --with-openssl=../openssl-1.1.0g

make install
```
