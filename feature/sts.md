```
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fstream>
#include <map>
#include <list>
extern "C"{
#include <curl/curl.h>
}
#include "common/ceph_crypto.h"
#include "include/str_list.h"
#include "common/ceph_json.h"
#include "common/code_environment.h"
#include "common/ceph_argparse.h"
#include "common/Finisher.h"
#include "global/global_init.h"
#include "rgw/rgw_common.h"
#include "rgw/rgw_bucket.h"
#include "rgw/rgw_rados.h"
#include "include/utime.h"
#include "include/object.h"
#include "cls/statelog/cls_statelog_types.h"
#include "cls/rgw/cls_rgw_ops.h"
#include "cls/rgw/cls_rgw_client.h"
#include "objclass/objclass.h"
#include <errno.h>
#include <string>
#include <sstream>
#include <cstdio>
#include <include/compat.h>
#include <gtest/gtest.h>
using namespace std;

RGWRados *store;

int main(int argc, char *argv[]){
  vector<const char*> args;
  args.push_back("--conf=/var/yuliyang/ceph/build/cluster1/ceph.conf");
  auto cct = global_init(NULL, args, CEPH_ENTITY_TYPE_CLIENT,
			 CODE_ENVIRONMENT_UTILITY,
			 CINIT_FLAG_NO_DEFAULT_CONFIG_FILE);
  common_init_finish(g_ceph_context);
  store = RGWStoreManager::get_storage(g_ceph_context, false, false, false, false, false);
  ::testing::InitGoogleTest(&argc, argv);
  int r = RUN_ALL_TESTS();
  return 0;
}

//TEST  (test1, run1) {
//  auto& pool = store->get_zone_params().sts_pool;
//  librados::IoCtx *ctx = store->get_sts_pool_ctx();
//  std::pair<string, int> entry("yly", 123);
//  std::string oid = "sts.0";
//  int ret = cls_rgw_sts_set_entry(*ctx, oid, entry);
//  if (ret >= 0) {
//    std::cout << " success " << std::endl;
//  }
//}

TEST  (test1, run2) {
  auto& pool = store->get_zone_params().sts_pool;
  librados::IoCtx *ctx = store->get_sts_pool_ctx();
  std::set<std::string> keys;
  std::map<std::string, bufferlist> omap;
  keys.insert("yly");
  ctx->omap_get_vals_by_keys("sts.0", keys, &omap);
  auto it = omap.find("yly");
  bufferlist *in = &(*it).second;
  auto iter = in->cbegin();
  std::pair<string, int> entry;
  try {
    decode(entry, iter);
    std::cout << entry.first << " ------ " << entry.second << std::endl;
  } catch (const buffer::error &err) {
    std::cout << "decode error" << std::endl;
    return ;
  }
}
```

```
./bin/ceph_test_rgw_yly
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from test1
[ RUN      ] test1.run1
yly ------ 123
[       OK ] test1.run1 (10 ms)
[----------] 1 test from test1 (10 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (10 ms total)
[  PASSED  ] 1 test.
```

```
./bin/rados -p default.rgw.log put sts.0 sts.0  --namespace=sts  -c cluster1/ceph.conf

./bin/rados -p default.rgw.log ls  --namespace=sts  -c cluster1/ceph.conf
sts.0

./bin/rados -p default.rgw.log listomapkeys  sts.0  --namespace=sts  -c cluster1/ceph.conf
yly

./bin/rados -p default.rgw.log getomapval sts.0 yly --namespace=sts  -c cluster1/ceph.conf
value (11 bytes) :
00000000  03 00 00 00 79 6c 79 7b  00 00 00                 |....yly{...|
0000000b

```
