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
  std::string url(argv[1]);
  regex regex_url("^(http|https)://(([a-z0-9A-Z])(([a-zA-Z0-9-]{1,61})?[a-zA-Z0-9]{1})?(\\.[a-zA-Z0-9](([a-zA-Z0-9-]{1,61})?[a-zA-Z0-9]{1})?)?(\\.[a-zA-ZA-Z]{2,4})+|((?:(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))\\.){3}(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))))((:([1-9][0-9]*))/|/)(.*)");
  cmatch m;
  if (regex_match(url.c_str(), m, regex_url)){
     std::cout<<"match\n"<< m[0] << std::endl;
  } else {
     std::cout<<"not match"<<std::endl;
  }
}
```

```
./regexdemo http://www.baidu.com.comm:90/aa
match
http://www.baidu.com.comm:90/aa
```

```
http://Zww.baidu.com:90/aa  <=match
http://www.baidu.com:abc/aa
http://www.baidu.com/aa  <=match
http://127.0.0.1/aa      <=match
http://127.0.0.1:98/aa   <=match
http://127.0.0.1:9c8/aa
http://10.2.2.2.2:98/aa
www.baidu.com
http://www.baidu.com.comm:90/aa   <=match
http://www.baidu.com.comm:9a2/aa
http://127.0.0.1:918
http://127.0.0.1/index.php   <=match
```


```
cmake_minimum_required(VERSION 3.12)
project(untitled1)

set(CMAKE_CXX_STANDARD 14)

include_directories(/home/onest/ceph/build/boost/include)
link_directories (/home/onest/ceph/build/boost/lib)


add_executable(untitled1 main.cpp)
target_link_libraries(untitled1 boost_filesystem boost_system boost_context)


#include <iostream>
#include <boost/coroutine2/all.hpp>

void foo(boost::coroutines2::coroutine<void>::push_type & sink){
  std::cout << "a ";
  sink();
  std::cout << "b ";
  sink();
  std::cout << "c ";
}

int main(){
  boost::coroutines2::coroutine<void>::pull_type source(foo);
  std::cout << "1 ";
  source();
  std::cout << "2 ";
  source();
  std::cout << "3 ";
  getchar();
  return 0;
}
```
