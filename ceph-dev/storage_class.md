
```
seq 1 5  | xargs -I{} -P 5 s3cmd  put 20M s3://test6/20M_ST_{} --storage-class=STANDARD  --multipart-chunk-size-mb=25
```

```
TEST  (test1, run1) {
bool is_truncated;
int ret;
RGWBucketInfo bucket_info;
RGWObjectCtx obj_ctx(store);
store->get_bucket_info(obj_ctx, "", "test6", bucket_info, NULL, NULL);
RGWRados::Bucket target(store, bucket_info);
RGWRados::Bucket::List list_op(&target);
vector<rgw_bucket_dir_entry> objs;
list_op.params.list_versions = bucket_info.versioned();
list_op.params.allow_unordered = true;
do {
    objs.clear();
    list_op.params.marker = list_op.get_next_marker();
    ret = list_op.list_objects(1000, &objs, NULL, &is_truncated);
    if (ret < 0) {
      std::cout << "ERROR: store->list_objects():" << std::endl;
      return;
    }
    for (auto obj_iter = objs.begin(); obj_iter != objs.end(); ++obj_iter) {
      rgw_obj_key key(obj_iter->key);
      rgw_obj obj(bucket_info.bucket, key);
      std::cout << obj_iter->key  << "  obj_iter->meta.storage_class: " << obj_iter->meta.storage_class << std::endl;
    } /* for objs */
} while (is_truncated);
}
```
