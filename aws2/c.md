
调试libs3
```
DEBUG=true make install

cmake_minimum_required(VERSION 3.7.1)
project(untitled6 C)
set(CMAKE_C_STANDARD 99)
add_executable(untitled6 main.c)
target_link_libraries(untitled6 libs3.a xml2 z m dl curl pthread)
```
