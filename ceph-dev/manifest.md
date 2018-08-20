```
static int init_bucket(const string& tenant_name, const string& bucket_name, const string& bucket_id,
                       RGWBucketInfo& bucket_info, rgw_bucket& bucket, map<string, bufferlist> *pattrs = nullptr)
{
  if (!bucket_name.empty()) {
    RGWObjectCtx obj_ctx(store);
    int r;
    if (bucket_id.empty()) {
      r = store->get_bucket_info(obj_ctx, tenant_name, bucket_name, bucket_info, nullptr, pattrs);
    } else {
      string bucket_instance_id = bucket_name + ":" + bucket_id;
      r = store->get_bucket_instance_info(obj_ctx, bucket_instance_id, bucket_info, NULL, pattrs);
    }
    if (r < 0) {
      return r;
    }
    bucket = bucket_info.bucket;
  }
  return 0;
}

```
```
TEST (json, test2){
  string bucket_id;
  rgw_bucket bucket;
  RGWBucketInfo bucket_info;
  map<string, bufferlist> attrs;
  int ret = init_bucket("", "test1", bucket_id, bucket_info, bucket);
  rgw_obj obj(bucket, "1M");
  uint64_t obj_size;
  RGWObjectCtx obj_ctx(store);
  RGWRados::Object op_target(store, bucket_info, obj_ctx, obj);
  RGWRados::Object::Read read_op(&op_target);

  read_op.params.attrs = &attrs;
  read_op.params.obj_size = &obj_size;

  ret = read_op.prepare();
  map<string, bufferlist>::iterator iter;
  iter = attrs.find(RGW_ATTR_MANIFEST);
  RGWObjManifest manifest;

  try {
    bufferlist& bl = iter->second;
    auto biter = bl.cbegin();
    decode(manifest, biter);
    std::cout << manifest.using_tail_data_pool << std::endl;
  } catch (buffer::error& err) {
  }
}
```

```
TEST (json, test2){
  string bucket_id;
  rgw_bucket bucket;
  RGWBucketInfo bucket_info;
  map<string, bufferlist> attrs;
  int ret = init_bucket("", "test1", bucket_id, bucket_info, bucket);
  rgw_obj obj(bucket, "5M");
  uint64_t obj_size;
  RGWObjectCtx obj_ctx(store);
  RGWRados::Object op_target(store, bucket_info, obj_ctx, obj);
  RGWRados::Object::Read read_op(&op_target);

  read_op.params.attrs = &attrs;
  read_op.params.obj_size = &obj_size;

  ret = read_op.prepare();
  map<string, bufferlist>::iterator iter;
  iter = attrs.find(RGW_ATTR_MANIFEST);
  RGWObjManifest manifest;

  try {
    bufferlist& bl = iter->second;
    auto biter = bl.cbegin();
    decode(manifest, biter);
    std::cout << manifest.using_tail_data_pool << std::endl;
  } catch (buffer::error& err) {
  }
}
```

```
TEST (json, test3){
  string bucket_id;
  rgw_bucket bucket;
  RGWBucketInfo bucket_info;
  map<string, bufferlist> attrs;
  int ret = init_bucket("", "test1", bucket_id, bucket_info, bucket);
  rgw_obj obj(bucket, "16M");
  uint64_t obj_size;
  RGWObjectCtx obj_ctx(store);
  RGWRados::Object op_target(store, bucket_info, obj_ctx, obj);
  RGWRados::Object::Read read_op(&op_target);

  read_op.params.attrs = &attrs;
  read_op.params.obj_size = &obj_size;

  ret = read_op.prepare();
  map<string, bufferlist>::iterator iter;
  iter = attrs.find(RGW_ATTR_MANIFEST);
  RGWObjManifest manifest;

  try {
    bufferlist& bl = iter->second;
    auto biter = bl.cbegin();
    decode(manifest, biter);
    std::cout << manifest.using_tail_data_pool << std::endl;
  } catch (buffer::error& err) {
  }
}
```

```
[==========] Running 3 tests from 1 test case.
[----------] Global test environment set-up.
[----------] 3 tests from json
[ RUN      ] json.test1
0
[       OK ] json.test1 (17 ms)
[ RUN      ] json.test2
1
[       OK ] json.test2 (4 ms)
[ RUN      ] json.test3
1
[       OK ] json.test3 (4 ms)
[----------] 3 tests from json (25 ms total)

[----------] Global test environment tear-down
[==========] 3 tests from 1 test case ran. (25 ms total)
[  PASSED  ] 3 tests.


```

