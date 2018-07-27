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
  std::string url = "http://127.0.0.1/index.php";
  regex regex_url("^(http|https)://((\\w+\\.)*\\w+(:[0-9][1-9]*)?)((/\\w*)*)(/\\w+\\.\\w+)?");
  cmatch m;
  if (regex_match(url.c_str(), m, regex_url)){
     std::cout<<"match"<<std::endl;
  } else {
     std::cout<<"not match"<<std::endl;
  }
}
```
