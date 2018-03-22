
radosgw-admin无法删除桶
```
./radosgw-admin bucket rm --bucket=q7uafu7dkd284tesw12ra4yitqwnr1203 --purge-objects --debug-rgw=20 --rgw-cache-enabled=false

#日志
0 cls_bucket_list q7uafu7dkd284tesw12ra4yitqwnr1203(@{i=default.rgw.buckets.index,e=default.rgw.buckets.non-ec}default.rgw.buckets.data[38404de9-508a-4eab-94d5-0f67d8e1eb96.54099.213]) start [] num_entries 1000
2018-03-22 08:48:33.218203 7f4a1ec3c9c0 20 reading from default.rgw.data.root:.bucket.meta.q7uafu7dkd284tesw12ra4yitqwnr1203:38404de9-508a-4eab-94d5-0f67d8e1eb96.54099.213
2018-03-22 08:48:33.218222 7f4a1ec3c9c0 20 get_system_obj_state: rctx=0x7ffdacd0c390 obj=default.rgw.data.root:.bucket.meta.q7uafu7dkd284tesw12ra4yitqwnr1203:38404de9-508a-4eab-94d5-0f67d8e1eb96.54099.213 state=0x55e0fd1a45d8 s->prefetch_data=0
2018-03-22 08:48:33.219508 7f4a1ec3c9c0 20 get_system_obj_state: s->obj_tag was set empty
2018-03-22 08:48:33.219597 7f4a1ec3c9c0 20 rados->read ofs=0 len=524288
2018-03-22 08:48:33.220685 7f4a1ec3c9c0 20 rados->read r=0 bl.length=376
2018-03-22 08:48:33.222941 7f4a1ec3c9c0 10 RGWRados::cls_bucket_list: got ___[]
2018-03-22 08:48:33.222998 7f4a1ec3c9c0 -1 ERROR: could not remove bucket q7uafu7dkd284tesw12ra4yitqwnr1203
2018-03-22 08:48:33.237214 7f4a1ec3c9c0  0 lockdep stop
```
有对象__
s3://q7uafu7dkd284tesw12ra4yitqwnr1203/__

待确认是否admin接口无法删除__对象
