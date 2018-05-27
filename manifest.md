```
./bin/rados -c ceph.conf  -p default.rgw.buckets.data getxattr   84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1_5M user.rgw.manifest > manifest
./bin/ceph-dencoder  type  RGWObjManifest import manifest decode dump_json
{
    "objs": [],
    "obj_size": 5242880,
    "explicit_objs": "false",
    "head_size": 4194304,
    "max_head_size": 4194304,
    "prefix": ".x4B81IdPE-TmwREMv-tDS7fH7e9nX7R_",
    "rules": [
        {
            "key": 0,
            "val": {
                "start_part_num": 0,
                "start_ofs": 4194304,
                "part_size": 0,
                "stripe_max_size": 4194304,
                "override_prefix": ""
            }
        }
    ],
    "tail_instance": "",
    "tail_placement": {
        "bucket": {
            "name": "test1",
            "marker": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
            "bucket_id": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
            "tenant": "",
            "explicit_placement": {
                "data_pool": "",
                "data_extra_pool": "",
                "index_pool": ""
            }
        },
        "placement_rule": "default-placement"
    },
    "begin_iter": {
        "part_ofs": 0,
        "stripe_ofs": 0,
        "ofs": 0,
        "stripe_size": 4194304,
        "cur_part_id": 0,
        "cur_stripe": 0,
        "cur_override_prefix": "",
        "location": {
            "placement_rule": "default-placement",
            "obj": {
                "bucket": {
                    "name": "test1",
                    "marker": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
                    "bucket_id": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
                    "tenant": "",
                    "explicit_placement": {
                        "data_pool": "",
                        "data_extra_pool": "",
                        "index_pool": ""
                    }
                },
                "key": {
                    "name": "5M",
                    "instance": "",
                    "ns": ""
                }
            },
            "raw_obj": {
                "pool": "",
                "oid": "",
                "loc": ""
            },
            "is_raw": false
        }
    },
    "end_iter": {
        "part_ofs": 4194304,
        "stripe_ofs": 4194304,
        "ofs": 5242880,
        "stripe_size": 1048576,
        "cur_part_id": 0,
        "cur_stripe": 1,
        "cur_override_prefix": "",
        "location": {
            "placement_rule": "default-placement",
            "obj": {
                "bucket": {
                    "name": "test1",
                    "marker": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
                    "bucket_id": "84e42446-57b5-410a-91f7-f0bcaea44a3c.4133.1",
                    "tenant": "",
                    "explicit_placement": {
                        "data_pool": "",
                        "data_extra_pool": "",
                        "index_pool": ""
                    }
                },
                "key": {
                    "name": ".x4B81IdPE-TmwREMv-tDS7fH7e9nX7R_1",
                    "instance": "",
                    "ns": "shadow"
                }
            },
            "raw_obj": {
                "pool": "",
                "oid": "",
                "loc": ""
            },
            "is_raw": false
        }
    }
}

```
