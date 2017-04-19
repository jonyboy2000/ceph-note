openssl pthread math
```
cmake_minimum_required(VERSION 3.6)
project(threaddemo2)
find_library(PTHREAD_LIBRARY pthread)
find_library(MATH_LIBRARY m)
find_library(OPENSSL_LIBRARIES crypto)
set(CMAKE_C_STANDARD 99)
set(SOURCE_FILES test.c)
add_executable(threaddemo2 ${SOURCE_FILES})
target_link_libraries(threaddemo2 ${OPENSSL_LIBRARIES} ${PTHREAD_LIBRARY} ${MATH_LIBRARY} )
```
