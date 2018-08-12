
上传1.txt到存储池test

```
#终端1
./bin/ceph osd pool create test 8 8 -c cluster1/ceph.conf
./bin/rados put -p test 1.txt 1.txt  -c cluster1/ceph.conf
./bin/rados -p test watch 1.txt -c cluster1/ceph.conf

#终端2
./bin/rados -p test notify 1.txt -c cluster1/ceph.conf "hello world"
```


#c++ 代码
## 公共部分
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
#include <gtest/gtest.h>
#define XMLNS_AWS_S3 "http://s3.amazonaws.com/doc/2006-03-01/"
#include "cat.h"

using namespace std;

RGWRados *store;

int main(int argc, char *argv[]){
  vector<const char*> args;
  args.push_back("--conf=/ceph/ceph/build/cluster1/ceph.conf");
  auto cct = global_init(NULL, args, CEPH_ENTITY_TYPE_CLIENT,
             CODE_ENVIRONMENT_UTILITY,
             CINIT_FLAG_NO_DEFAULT_CONFIG_FILE);
  common_init_finish(g_ceph_context);
  store = RGWStoreManager::get_storage(g_ceph_context, false, false, false, false, false);
  ::testing::InitGoogleTest(&argc, argv);
  int r = RUN_ALL_TESTS();
  return 0;
}
```

## watch
```
class RadosWatchCtx : public librados::WatchCtx2 {
  librados::IoCtx& ioctx;
  std::string name;
public:
  RadosWatchCtx(librados::IoCtx& io, const char *_name) : ioctx(io), name(_name) {}
  ~RadosWatchCtx() override {}
  void handle_notify(uint64_t notify_id,
                     uint64_t cookie,
                     uint64_t notifier_id,
                     bufferlist& bl) override {
    std::cout << "NOTIFY"
         << " cookie " << cookie
         << " notify_id " << notify_id
         << " from " << notifier_id
         << std::endl;
    bl.hexdump(cout);
    ioctx.notify_ack(name, notify_id, cookie, bl);
  }
  void handle_error(uint64_t cookie, int err) override {
    std::cout << "ERROR"
         << " cookie " << cookie
         << std::endl;
  }
};

TEST (watch, watch1) {
  librados::Rados *rados = store->get_rados_handle();
  librados::IoCtx io_ctx; //rados_ioctx_t
  int ret = store->get_rados_handle()->ioctx_create("test", io_ctx);
  string oid("1.txt");
  RadosWatchCtx ctx(io_ctx, oid.c_str());
  uint64_t cookie;
  ret = io_ctx.watch2(oid, &cookie, &ctx);
  if (ret != 0)
    std::cout << "error calling watch: " << std::endl;
  else {
    std::cout << "press enter to exit..." << std::endl;
    getchar();
    io_ctx.unwatch2(cookie);
    rados->watch_flush();
  }
}
```

## notify
```
TEST  (notify, notify1) {
  librados::IoCtx io_ctx;  
  int ret = store->get_rados_handle()->ioctx_create("test", io_ctx);
  string oid("1.txt");
  string msg("hello world");
  bufferlist bl, replybl;
  encode(msg, bl);
  ret = io_ctx.notify2(oid, bl, 10000, &replybl);
  if (ret != 0)
    std::cout << "error calling notify" << std::endl;
  if (replybl.length()) {
    map<pair<uint64_t,uint64_t>,bufferlist> rm;
    set<pair<uint64_t,uint64_t> > missed;
    auto p = replybl.cbegin();
    decode(rm, p);
    decode(missed, p);
    for (map<pair<uint64_t,uint64_t>,bufferlist>::iterator p = rm.begin();
    p != rm.end();
    ++p) {
      std::cout << "reply client." << p->first.first
      << " cookie " << p->first.second
      << " : " << p->second.length() << " bytes" << std::endl;
      if (p->second.length())
      p->second.hexdump(cout);
    }
    for (multiset<pair<uint64_t,uint64_t> >::iterator p = missed.begin();
    p != missed.end(); ++p) {
      std::cout << "timeout client." << p->first
      << " cookie " << p->second << std::endl;
    }
  }
}
```
