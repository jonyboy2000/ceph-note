CMakeLists.txt
```
cmake_minimum_required(VERSION 2.8)
project(regexdemo)

set(CMAKE_CXX_STANDARD 11)

include_directories(/root/ceph/build/boost/include)
link_directories (/root/ceph/build/boost/lib)

set(SOURCE_FILES main.cpp)
add_executable(regexdemo ${SOURCE_FILES})
target_link_libraries(regexdemo boost_filesystem boost_system boost_regex)
```

main.cpp
```
#include <iostream>
#include <boost/regex.hpp>
using namespace boost;
using namespace std;
int main(int argc, char* argv[]){
  std::string url = "http://www.baidu.com/aaa";
//  std::string url = "http://www.baidu.com/aaa,http://www.abc.com/bbb";
  regex regex_url("^(http|https)://([^:]*)(:\\d*)?");
  cmatch m;
  if (regex_match(url.c_str(), m, regex_url)){
     std::cout<<"111"<<std::endl;
  } else {
     std::cout<<"222"<<std::endl;
  }
}
```
