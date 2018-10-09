
```
yum install -y systemtap systemtap-runtime

yum install http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-3.10.0-327.el7.x86_64.rpm http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-common-x86_64-3.10.0-327.el7.x86_64.rpm
https://buildlogs.centos.org/c7.1511.00/kernel/20151119220809/3.10.0-327.el7.x86_64/kernel-devel-3.10.0-327.el7.x86_64.rpm

yum install http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-3.10.0-327.28.3.el7.x86_64.rpm http://ftp.riken.jp/Linux/cern/centos/7.2/updates/Debug/x86_64/kernel-debuginfo-common-x86_64-3.10.0-327.28.3.el7.x86_64.rpm
ftp://ftp.pbone.net/mirror/ftp.scientificlinux.org/linux/scientific/7.2/x86_64/updates/security/kernel-devel-3.10.0-327.28.3.el7.x86_64.rpm

stap -v -e 'probe vfs.read {printf("read performed\n"); exit()}'
```

```

cat rgw.stp 
probe process("/root/ceph/build/bin/radosgw").function("*@*rgw_process.cc*").call
{
  printf("%s\n", pp());
}

stap -x 1270 rgw.stp   #upload by s3cmd put 1.txt s3://test1
process("/root/ceph/build/bin/radosgw").function("process_request@/root/ceph/src/rgw/rgw_process.cc:121").call
process("/root/ceph/build/bin/radosgw").function("rgw_process_authenticated@/root/ceph/src/rgw/rgw_process.cc:37").call
```

cat rgw2.stp 
```
probe process("/root/ceph/build/bin/radosgw").function("*@*rgw_process.cc*").call
, process("/root/ceph/build/bin/radosgw").function("*@*rgw_op.cc*").call
, process("/root/ceph/build/bin/radosgw").function("*@*rgw_rest_*").call
{
  printf("%s\n", pp());
}
```

```
stap -x 1270 rgw2.stp  #1270为rgw进程号
process("/root/ceph/build/bin/radosgw").function("process_request@/root/ceph/src/rgw/rgw_process.cc:121").call
process("/root/ceph/build/bin/radosgw").function("looks_like_ip_address@/root/ceph/src/rgw/rgw_rest_s3.h:608").call
process("/root/ceph/build/bin/radosgw").function("get_handler@/root/ceph/src/rgw/rgw_rest_s3.cc:3479").call
process("/root/ceph/build/bin/radosgw").function("init_from_header@/root/ceph/src/rgw/rgw_rest_s3.cc:3213").call
process("/root/ceph/build/bin/radosgw").function("RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:587").call
process("/root/ceph/build/bin/radosgw").function("RGWHandler_REST_S3@/root/ceph/src/rgw/rgw_rest_s3.h:506").call
process("/root/ceph/build/bin/radosgw").function("init@/root/ceph/src/rgw/rgw_rest_s3.cc:3349").call
process("/root/ceph/build/bin/radosgw").function("init@/root/ceph/src/rgw/rgw_op.cc:6983").call
process("/root/ceph/build/bin/radosgw").function("op_put@/root/ceph/src/rgw/rgw_rest_s3.cc:3170").call
process("/root/ceph/build/bin/radosgw").function("is_acl_op@/root/ceph/src/rgw/rgw_rest_s3.h:569").call
process("/root/ceph/build/bin/radosgw").function("is_tagging_op@/root/ceph/src/rgw/rgw_rest_s3.h:572").call
process("/root/ceph/build/bin/radosgw").function("RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:209").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("authorize@/root/ceph/src/rgw/rgw_rest_s3.h:515").call
process("/root/ceph/build/bin/radosgw").function("authorize@/root/ceph/src/rgw/rgw_rest_s3.cc:3446").call
process("/root/ceph/build/bin/radosgw").function("is_applicable@/root/ceph/src/rgw/rgw_rest_s3.cc:4289").call
process("/root/ceph/build/bin/radosgw").function("discover_aws_flavour@/root/ceph/src/rgw/rgw_rest_s3.cc:3405").call
process("/root/ceph/build/bin/radosgw").function("authenticate@/root/ceph/src/rgw/rgw_rest_s3.cc:4116").call
process("/root/ceph/build/bin/radosgw").function("get_auth_data@/root/ceph/src/rgw/rgw_rest_s3.cc:3783").call
process("/root/ceph/build/bin/radosgw").function("discover_aws_flavour@/root/ceph/src/rgw/rgw_rest_s3.cc:3405").call
process("/root/ceph/build/bin/radosgw").function("get_auth_data_v2@/root/ceph/src/rgw/rgw_rest_s3.cc:3995").call
process("/root/ceph/build/bin/radosgw").function("authenticate@/root/ceph/src/rgw/rgw_rest_s3.cc:4237").call
process("/root/ceph/build/bin/radosgw").function("null_completer_factory@/root/ceph/src/rgw/rgw_rest_s3.cc:3776").call
process("/root/ceph/build/bin/radosgw").function("~auth_data_t@/root/ceph/src/rgw/rgw_rest_s3.h:720").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("postauth_init@/root/ceph/src/rgw/rgw_rest_s3.cc:3306").call
process("/root/ceph/build/bin/radosgw").function("valid_s3_bucket_name@/root/ceph/src/rgw/rgw_rest_s3.h:641").call
process("/root/ceph/build/bin/radosgw").function("looks_like_ip_address@/root/ceph/src/rgw/rgw_rest_s3.h:608").call
process("/root/ceph/build/bin/radosgw").function("rgw_process_authenticated@/root/ceph/src/rgw/rgw_process.cc:37").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("do_init_permissions@/root/ceph/src/rgw/rgw_op.cc:6993").call
process("/root/ceph/build/bin/radosgw").function("rgw_build_bucket_policies@/root/ceph/src/rgw/rgw_op.cc:395").call
process("/root/ceph/build/bin/radosgw").function("read_bucket_policy@/root/ceph/src/rgw/rgw_op.cc:308").call
process("/root/ceph/build/bin/radosgw").function("get_bucket_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:260").call
process("/root/ceph/build/bin/radosgw").function("get_bucket_instance_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:195").call
process("/root/ceph/build/bin/radosgw").function("decode_policy@/root/ceph/src/rgw/rgw_op.cc:156").call
process("/root/ceph/build/bin/radosgw").function("get_iam_policy_from_attr@/root/ceph/src/rgw/rgw_op.cc:269").call
process("/root/ceph/build/bin/radosgw").function("rgw_build_iam_environment@/root/ceph/src/rgw/rgw_op.cc:653").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("is_obj_update_op@/root/ceph/src/rgw/rgw_rest_s3.h:575").call
process("/root/ceph/build/bin/radosgw").function("is_acl_op@/root/ceph/src/rgw/rgw_rest_s3.h:569").call
process("/root/ceph/build/bin/radosgw").function("is_tagging_op@/root/ceph/src/rgw/rgw_rest_s3.h:572").call
process("/root/ceph/build/bin/radosgw").function("do_read_permissions@/root/ceph/src/rgw/rgw_op.cc:7006").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("init_quota@/root/ceph/src/rgw/rgw_op.cc:942").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("verify_op_mask@/root/ceph/src/rgw/rgw_op.cc:781").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("verify_permission@/root/ceph/src/rgw/rgw_op.cc:3090").call
process("/root/ceph/build/bin/radosgw").function("get_params@/root/ceph/src/rgw/rgw_rest_s3.cc:1270").call
process("/root/ceph/build/bin/radosgw").function("create_s3_policy@/root/ceph/src/rgw/rgw_rest_s3.cc:1100").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("pre_exec@/root/ceph/src/rgw/rgw_op.cc:3342").call
process("/root/ceph/build/bin/radosgw").function("rgw_bucket_object_pre_exec@/root/ceph/src/rgw/rgw_op.cc:710").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("execute@/root/ceph/src/rgw/rgw_op.cc:3463").call
process("/root/ceph/build/bin/radosgw").function("select_processor@/root/ceph/src/rgw/rgw_op.cc:3314").call
process("/root/ceph/build/bin/radosgw").function("get_encrypt_filter@/root/ceph/src/rgw/rgw_rest_s3.cc:1503").call
process("/root/ceph/build/bin/radosgw").function("get_data@/root/ceph/src/rgw/rgw_rest_s3.cc:1382").call
process("/root/ceph/build/bin/radosgw").function("get_data@/root/ceph/src/rgw/rgw_rest_s3.cc:1382").call
process("/root/ceph/build/bin/radosgw").function("do_aws4_auth_completion@/root/ceph/src/rgw/rgw_op.cc:923").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("do_aws4_auth_completion@/root/ceph/src/rgw/rgw_op.cc:923").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("populate_with_generic_attrs@/root/ceph/src/rgw/rgw_op.cc:2606").call
process("/root/ceph/build/bin/radosgw").function("dispose_processor@/root/ceph/src/rgw/rgw_op.cc:3337").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("send_response@/root/ceph/src/rgw/rgw_rest_s3.cc:1406").call
process("/root/ceph/build/bin/radosgw").function("generate_cors_headers@/root/ceph/src/rgw/rgw_op.cc:1083").call
process("/root/ceph/build/bin/radosgw").function("gen_prefix@/root/ceph/src/rgw/rgw_op.cc:7034").call
process("/root/ceph/build/bin/radosgw").function("~RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:210").call
process("/root/ceph/build/bin/radosgw").function("~RGWPutObj_ObjStore_S3@/root/ceph/src/rgw/rgw_rest_s3.h:210").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:588").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_Obj_S3@/root/ceph/src/rgw/rgw_rest_s3.h:588").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler_REST_S3@/root/ceph/src/rgw/rgw_rest_s3.h:510").call
process("/root/ceph/build/bin/radosgw").function("~RGWHandler@/root/ceph/src/rgw/rgw_op.cc:6979").call
```
