
```
s3cmd setacl s3://{存日志桶名字} --acl-grant=write:LogDeliver
s3cmd setacl s3://{存日志桶名字} --acl-grant=read_acp:LogDeliver
```

```
s3cmd -c yly.s3cfg setacl s3://beijing2-logging-loop --acl-grant=write:bl_deliver
s3cmd -c yly.s3cfg setacl s3://beijing2-logging-loop --acl-grant=read_acp:bl_deliver

from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
url = 'http://127.0.0.1:8083'
#url = 'http://172.20.243.26:8083'
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url)
bl =  {
        'LoggingEnabled': {
            'TargetBucket': 'beijing2-logging-loop',
            'TargetPrefix': 'logs/'
        }
    }
print s3_client.put_bucket_logging(Bucket="beijing2-logging-loop", BucketLoggingStatus = bl)


seq 1 20  | xargs -I{} -P 20 s3cmd -c yly.s3cfg  put onest.s3cfg s3://beijing2-logging-loop/1111111.{}.2222
```

```
bl =  {
        'LoggingEnabled': {
            'TargetBucket': '存日志桶名字',
            'TargetPrefix': '目录前缀/'
        }
    }
s3_client.put_bucket_logging(Bucket="桶名字", BucketLoggingStatus = bl)
```




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
#include <gtest/gtest.h>
using namespace std;

RGWRados *store;

int main(int argc, char *argv[]){
  vector<const char*> args;
  args.push_back("--conf=/etc/ceph/ceph.conf");
  auto cct = global_init(NULL, args, CEPH_ENTITY_TYPE_CLIENT,
			 CODE_ENVIRONMENT_UTILITY,
			 CINIT_FLAG_NO_DEFAULT_CONFIG_FILE);
  common_init_finish(g_ceph_context);
  store = RGWStoreManager::get_storage(g_ceph_context, false, false, false, false, false);
  ::testing::InitGoogleTest(&argc, argv);
  int r = RUN_ALL_TESTS();
  return 0;
}


TEST  (test1, run1) {
  auto& pool = store->get_zone_params().bl_pool;
  librados::IoCtx *ctx = store->get_bl_pool_ctx();
  std::set<std::string> keys;
  std::map<std::string, bufferlist> omap;
  keys.insert(":bucket00000001:a364ac55-8819-4660-8351-616bdca54d9a.2632135.5");
  ctx->omap_get_vals_by_keys("bl.6", keys, &omap);
  auto it = omap.find(":bucket00000001:a364ac55-8819-4660-8351-616bdca54d9a.2632135.5");
  bufferlist *in = &(*it).second;
  auto iter = in->begin();
  std::pair<string, int> entry;
  try {
    ::decode(entry, iter);
    std::cout << entry.first << " ------ " << entry.second << std::endl;
  } catch (const buffer::error &err) {
    std::cout << "decode error" << std::endl;
    return ;
  }
}
```

```
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from test1
[ RUN      ] test1.run1
:bucket00000001:a364ac55-8819-4660-8351-616bdca54d9a.2632135.5 ------ 5
[       OK ] test1.run1 (0 ms)
[----------] 1 test from test1 (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (0 ms total)
[  PASSED  ] 1 test.

```

```
const char* BL_STATUS[] = {
  "UNINITIAL",
  "PROCESSING",
  "FAILED",
  "PERM_ERROR",
  "ACL_ERROR",
  "COMPLETE"   <==5
};
```

```
[root@ceph68 ceph]# rados  -p default.rgw.bl listomapkeys  bl.6
:bucket00000001:a364ac55-8819-4660-8351-616bdca54d9a.2632135.5


rados  -p default.rgw.bl getomapval   bl.6 :bucket00000001:a364ac55-8819-4660-8351-616bdca54d9a.2632135.5
value (70 bytes) :
00000000  3e 00 00 00 3a 62 75 63  6b 65 74 30 30 30 30 30  |>...:bucket00000|
00000010  30 30 31 3a 61 33 36 34  61 63 35 35 2d 38 38 31  |001:a364ac55-881|
00000020  39 2d 34 36 36 30 2d 38  33 35 31 2d 36 31 36 62  |9-4660-8351-616b|
00000030  64 63 61 35 34 64 39 61  2e 32 36 33 32 31 33 35  |dca54d9a.2632135|
00000040  2e 35 05 00 00 00                                 |.5....|
00000046

```
