```
[root@BFJD-TESTN-ONEST001 ~]# ceph-request get "/admin/usage?format=json&show-entries=True&show-summary=True&uid=yly&network_id=outer&bucket=version" -c admin.request --pretty
{
    "entries": [
        {
            "buckets": [
                {
                    "bucket": "version",
                    "categories": [
                        {
                            "bytes_received": 0,
                            "bytes_sent": 0,
                            "category": "delete_obj",
                            "ops": 1,
                            "successful_ops": 1
                        },
                        {
                            "bytes_received": 0,
                            "bytes_sent": 2190,
                            "category": "get_acls",
                            "ops": 5,
                            "successful_ops": 5
                        },
                        {
                            "bytes_received": 0,
                            "bytes_sent": 548,
                            "category": "get_bucket_versioning",
                            "ops": 3,
                            "successful_ops": 3
                        },
                        {
                            "bytes_received": 0,
                            "bytes_sent": 20412,
                            "category": "list_bucket",
                            "ops": 21,
                            "successful_ops": 17
                        },
                        {
                            "bytes_received": 15,
                            "bytes_sent": 0,
                            "category": "put_obj",
                            "ops": 3,
                            "successful_ops": 3
                        },
                        {
                            "bytes_received": 152,
                            "bytes_sent": 38,
                            "category": "set_bucket_versioning",
                            "ops": 2,
                            "successful_ops": 2
                        }
                    ],
                    "epoch": 1540432800,
                    "owner": "yly",
                    "time": "2018-10-25 02:00:00.000000Z"
                }
            ],
            "user": "yly"
        }
    ],
    "summary": [
        {
            "categories": [
                {
                    "bytes_received": 0,
                    "bytes_sent": 0,
                    "category": "delete_obj",
                    "ops": 1,
                    "successful_ops": 1
                },
                {
                    "bytes_received": 0,
                    "bytes_sent": 2190,
                    "category": "get_acls",
                    "ops": 5,
                    "successful_ops": 5
                },
                {
                    "bytes_received": 0,
                    "bytes_sent": 548,
                    "category": "get_bucket_versioning",
                    "ops": 3,
                    "successful_ops": 3
                },
                {
                    "bytes_received": 0,
                    "bytes_sent": 20412,
                    "category": "list_bucket",
                    "ops": 21,
                    "successful_ops": 17
                },
                {
                    "bytes_received": 15,
                    "bytes_sent": 0,
                    "category": "put_obj",
                    "ops": 3,
                    "successful_ops": 3
                },
                {
                    "bytes_received": 152,
                    "bytes_sent": 38,
                    "category": "set_bucket_versioning",
                    "ops": 2,
                    "successful_ops": 2
                }
            ],
            "total": {
                "bytes_received": 167,
                "bytes_sent": 23188,
                "ops": 35,
                "successful_ops": 31
            },
            "user": "yly"
        }
    ]
}

```
