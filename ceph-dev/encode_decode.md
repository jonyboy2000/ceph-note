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
#include <gtest/gtest.h>
using namespace std;

RGWRados *store;

int main(int argc, char *argv[]){
  vector<const char*> args;
  args.push_back("--conf=/root/yehudasa/ceph/build/ceph.conf");
  auto cct = global_init(NULL, args, CEPH_ENTITY_TYPE_CLIENT,
			 CODE_ENVIRONMENT_UTILITY,
			 CINIT_FLAG_NO_DEFAULT_CONFIG_FILE);
  common_init_finish(g_ceph_context);
  store = RGWStoreManager::get_storage(g_ceph_context, false, false, false, false, false);
  ::testing::InitGoogleTest(&argc, argv);
  int r = RUN_ALL_TESTS();
  return 0;
}


struct multipart_upload_info
{
  string storage_class;
  void encode(bufferlist& bl) const {
    ENCODE_START(1, 1, bl);
    ceph::encode(storage_class, bl);
    ENCODE_FINISH(bl);
  }
  void decode(bufferlist::const_iterator& bl) {
    DECODE_START(1, bl);
    ceph::decode(storage_class, bl);
    DECODE_FINISH(bl);
  }
};
WRITE_CLASS_ENCODER(multipart_upload_info)

TEST  (test1, run1) {

librados::IoCtx io_ctx;
int ret = store->get_rados_handle()->ioctx_create("test", io_ctx);

librados::bufferlist bl;
multipart_upload_info upload_info;
upload_info.storage_class = "STANDARD_IA";
encode(upload_info, bl);

ret = io_ctx.write_full("hw", bl);
if (ret < 0) {
  std::cerr << "Couldn't write object! error " << ret << std::endl;
  exit(EXIT_FAILURE);
} else {
  std::cout << "Wrote new object 'hw' " << std::endl;
}

RGWBucketInfo src_bucket_info;
RGWObjectCtx obj_ctx(store);
rgw_obj obj;
store->get_bucket_info(obj_ctx, "", "test1", src_bucket_info, NULL, NULL);
map<string, bufferlist> xattrs;
RGWMPObj mp;
string upload_id = "2~FtLzzc9A4AzOMoRLp2KsWNQT7Ytlroz";
mp.init("multi", upload_id);
obj.init_ns(src_bucket_info.bucket, mp.get_meta(), "multipart");
obj.set_in_extra_data(true);
bufferlist bl;

RGWRados::Object op_target(store, src_bucket_info, obj_ctx, obj);
RGWRados::Object::Read read_op(&op_target);
read_op.params.attrs = &xattrs;

int ret = read_op.prepare();
if (ret < 0) {
  return;
}

ret = read_op.read(0, 4194304, bl);
multipart_upload_info info;

try {
  auto biter = bl.cbegin();
  decode(info, biter);
  std::cout << "xxxxxxxxxxxxxx:   " << info.storage_class << std::endl;
} catch (buffer::error& err) {
}







//RGWZoneParams zone("55a599e8-f2b0-41d6-a388-17a26ae16695", "default");
//int ret = zone.init(g_ceph_context, store);
//RGWZonePlacementInfo& info = zone.placement_pools["default-placement"];
//
//const RGWZoneStorageClass *storage_class;
//static rgw_pool no_pool;
//const string sc = "STANDARD_IA";
//if (!info.storage_classes.find(sc, &storage_class)) {
//std::cout << "not found" << std::endl;
//} else {
//std::cout << "found" << std::endl;
//}

// RGWBucketAdminOpState bucket_op;
// bucket_op.set_bucket_name("test1");
// int ret = RGWBucketAdminOp::dump_s3_policy(store, bucket_op, std::cout);

}
```
