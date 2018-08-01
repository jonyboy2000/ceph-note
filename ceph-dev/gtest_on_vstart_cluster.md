```
make cython_rados monmaptool ceph-mon ceph-osd radosgw radosgw-admin ceph-authtool ceph-conf crushtool monmaptool rados ceph-mgr ceph-dencoder

mkdir cluster1
CEPH_RGW_PORT=80 CEPH_NUM_OSD=1 CEPH_NUM_MON=1 CEPH_NUM_MGR=1  CEPH_NUM_MDS=0 CEPH_NUM_RGW=1 VSTART_DEST=cluster1  ../src/vstart.sh --new -x --localhost --without-dashboard --filestore

make gtest_main gtest
```

CMakeLists.txt
```
cmake_minimum_required(VERSION 3.7)
project(gtestrgwtest)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -D__STDC_FORMAT_MACROS")
set(CEPH-SRC /ceph/ceph)
include_directories(${CEPH-SRC}/src/googletest/googletest/include ${CEPH-SRC}/src ${CEPH-SRC}/src/include ${CEPH-SRC}/build/include ${CEPH-SRC}/build/boost/include)
link_directories (${CEPH-SRC}/build/lib ${CEPH-SRC}/build/boost/lib)

add_executable(gtestrgwtest main.cpp)
target_link_libraries(gtestrgwtest
        libgtest.a
        libgtest_main.a
        pthread
        rados
       )
```

main.cpp
```
#include <iostream>
#include <rados/librados.hpp>
#include "gtest/gtest.h"
using namespace librados;

TEST  (base,111) {
  int ret = 0;
  /* Declare the cluster handle and required variables. */
  librados::Rados cluster;
  char cluster_name[] = "ceph";
  char user_name[] = "client.admin";
  uint64_t flags;

  ret = cluster.init2(user_name, cluster_name, flags);
  if (ret < 0) {
    std::cerr << "Couldn't initialize the cluster handle! error " << ret << std::endl;
  } else {
    std::cout << "Created a cluster handle." << std::endl;
  }

  ret = cluster.conf_read_file("/ceph/ceph/build/cluster1/ceph.conf");
  if (ret < 0) {
    std::cerr << "Couldn't read the Ceph configuration file! error " << ret << std::endl;
  } else {
    std::cout << "Read the Ceph configuration file." << std::endl;
  }

  ret = cluster.connect();
  if (ret < 0) {
    std::cerr << "Couldn't connect to cluster! error " << ret << std::endl;
  } else {
    std::cout << "Connected to the cluster." << std::endl;
  }

  librados::IoCtx io_ctx;
  const char *pool_name = "default.rgw.buckets.index";
  int64_t pool_id = cluster.pool_lookup(pool_name);
  ret = cluster.ioctx_create2(pool_id, io_ctx);
  if (ret < 0) {
    std::cerr << "Couldn't set up ioctx! error " << ret << std::endl;
    exit(EXIT_FAILURE);
  } else {
    std::cout << "Created an ioctx for the pool." << std::endl;
  }

  std::set<std::string> out_keys;
  ret = io_ctx.omap_get_keys(".dir.40e130fe-7b12-44b7-ab9e-ce421b8fcd16.254103.1", "", LONG_MAX, &out_keys);
  if (ret < 0) {
    std::cout << "error getting omap key set " << pool_name << "/"
              << ".dir.40e130fe-7b12-44b7-ab9e-ce421b8fcd16.264117.3" << std::endl;
    exit(EXIT_FAILURE);
  }

  for (std::set<std::string>::iterator iter = out_keys.begin();
       iter != out_keys.end(); ++iter) {
    std::cout << *iter << std::endl;
  }
}

int main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

```

```
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from base
[ RUN      ] base.111
Created a cluster handle.
Read the Ceph configuration file.
Connected to the cluster.
Created an ioctx for the pool.
IA
ST
ST2
ST3
ST4
_multipart_IA_1M_6.2~FNVFaxnEsLp5HNeYp1OwugMaOWlUQ9Z.1
_multipart_IA_1M_6.2~FNVFaxnEsLp5HNeYp1OwugMaOWlUQ9Z.meta
prefix/keyv6
[       OK ] base.111 (344 ms)
[----------] 1 test from base (344 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (344 ms total)
[  PASSED  ] 1 test.
```

```
./bin/rados -p default.rgw.buckets.index listomapkeys .dir.40e130fe-7b12-44b7-ab9e-ce421b8fcd16.254103.1  -c  cluster1/ceph.conf
2018-08-01 08:40:13.872 7fbcd20dbb00 -1 WARNING: all dangerous and experimental features are enabled.
2018-08-01 08:40:13.929 7fbcd20dbb00 -1 WARNING: all dangerous and experimental features are enabled.
2018-08-01 08:40:13.956 7fbcd20dbb00 -1 WARNING: all dangerous and experimental features are enabled.
IA
ST
ST2
ST3
ST4
_multipart_IA_1M_6.2~FNVFaxnEsLp5HNeYp1OwugMaOWlUQ9Z.1
_multipart_IA_1M_6.2~FNVFaxnEsLp5HNeYp1OwugMaOWlUQ9Z.meta
prefix/keyv6

```
