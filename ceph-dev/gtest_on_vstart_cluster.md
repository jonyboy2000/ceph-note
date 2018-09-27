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

TEST  (test1, run_this_test) {   //TEST  (test1, DISABLED_no_run) { 
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


```
TEST  (writeandread, run1) {
  librados::IoCtx io_ctx; 
  int ret = store->get_rados_handle()->ioctx_create("test", io_ctx);
  librados::bufferlist bl;
  bl.append("Hello World!");
  ret = io_ctx.write_full("hw", bl);
  if (ret < 0) {
    std::cerr << "Couldn't write object! error " << ret << std::endl;
    exit(EXIT_FAILURE);
  } else {
    std::cout << "Wrote new object 'hw' " << std::endl;
  }
  librados::bufferlist read_buf;
  int read_len = 4194304;
  //Create I/O Completion.
  librados::AioCompletion *read_completion = librados::Rados::aio_create_completion();
  //Send read request.
  ret = io_ctx.aio_read("hw", read_completion, &read_buf, read_len, 0);
  if (ret < 0) {
    std::cerr << "Couldn't start read object! error " << ret << std::endl;
    exit(EXIT_FAILURE);
  }
  // Wait for the request to complete, and check that it succeeded.
  read_completion->wait_for_complete();
  ret = read_completion->get_return_value();
  if (ret < 0) {
    std::cerr << "Couldn't read object! error " << ret << std::endl;
    exit(EXIT_FAILURE);
  } else {
    std::cout << "Read object hw asynchronously with contents.\n"
    << read_buf.c_str() << std::endl;
  }
}


[root@promote build]# ./bin/ceph_test_yly
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from writeandread
[ RUN      ] writeandread.run1
Wrote new object 'hw'
Read object hw asynchronously with contents.
Hello World!
[       OK ] writeandread.run1 (10 ms)
[----------] 1 test from writeandread (10 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (10 ms total)
[  PASSED  ] 1 test.

  YOU HAVE 5 DISABLED TESTS  
```

```
  RGWBucketInfo src_bucket_info;
  RGWObjectCtx obj_ctx(store);
  rgw_obj obj;
  store->get_bucket_info(obj_ctx, "", "test1", src_bucket_info, NULL, NULL);
  obj = rgw_obj(src_bucket_info.bucket, "16M");

  RGWRados::Object op_target(store, src_bucket_info, obj_ctx, obj);
  RGWRados::Object::Read read_op(&op_target);
  uint64_t obj_size;
  read_op.params.obj_size = &obj_size;
  ceph::real_time lastmod;
  read_op.params.lastmod = &lastmod;
  int op_ret = read_op.prepare();
  ceph::real_time current = ceph::real_clock::now();

  std::cout << "obj_size = " << obj_size << std::endl;
  std::cout << "lastmod = " << lastmod << std::endl;
  std::cout << "current = " << current << std::endl;

  double timediff;
  timediff = ceph::real_clock::to_time_t(current) - ceph::real_clock::to_time_t(lastmod);
  std::cout << "timediff = " << timediff << std::endl;
```
