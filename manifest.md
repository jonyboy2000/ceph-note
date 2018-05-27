```
5M
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


```
14M
{
    "objs": [],
    "obj_size": 14680064,
    "explicit_objs": "false",
    "head_size": 4194304,
    "max_head_size": 4194304,
    "prefix": ".24I5EmMofHcdbm6DhPocBMw62RIXke__",
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
                    "name": "14M",
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
        "stripe_ofs": 12582912,
        "ofs": 14680064,
        "stripe_size": 2097152,
        "cur_part_id": 0,
        "cur_stripe": 3,
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
                    "name": ".24I5EmMofHcdbm6DhPocBMw62RIXke__3",
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



```
16M
{
    "objs": [],
    "obj_size": 16777216,
    "explicit_objs": "false",
    "head_size": 0,
    "max_head_size": 0,
    "prefix": "16M.2~HqkbU-7RW_LJATJBASWYrTXAcBiC-MD",
    "rules": [
        {
            "key": 0,
            "val": {
                "start_part_num": 1,
                "start_ofs": 0,
                "part_size": 15728640,
                "stripe_max_size": 4194304,
                "override_prefix": ""
            }
        },
        {
            "key": 15728640,
            "val": {
                "start_part_num": 2,
                "start_ofs": 15728640,
                "part_size": 1048576,
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
        "cur_part_id": 1,
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
                    "name": "16M.2~HqkbU-7RW_LJATJBASWYrTXAcBiC-MD.1",
                    "instance": "",
                    "ns": "multipart"
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
        "part_ofs": 16777216,
        "stripe_ofs": 16777216,
        "ofs": 16777216,
        "stripe_size": 1048576,
        "cur_part_id": 3,
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
                    "name": "16M.2~HqkbU-7RW_LJATJBASWYrTXAcBiC-MD.3",
                    "instance": "",
                    "ns": "multipart"
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

```
20M
{
    "objs": [],
    "obj_size": 20971520,
    "explicit_objs": "false",
    "head_size": 0,
    "max_head_size": 0,
    "prefix": "20M.2~uO9gV71ALyIu6DDieeCRzI06zZQ9L1u",
    "rules": [
        {
            "key": 0,
            "val": {
                "start_part_num": 1,
                "start_ofs": 0,
                "part_size": 15728640,
                "stripe_max_size": 4194304,
                "override_prefix": ""
            }
        },
        {
            "key": 15728640,
            "val": {
                "start_part_num": 2,
                "start_ofs": 15728640,
                "part_size": 5242880,
                "stripe_max_size": 4194304,
                "override_prefix": ""
            }
        }
    ],
    "tail_instance": "",
    "tail_placement": {
        "bucket": {
            "name": "test1",
            "marker": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
            "bucket_id": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
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
        "cur_part_id": 1,
        "cur_stripe": 0,
        "cur_override_prefix": "",
        "location": {
            "placement_rule": "default-placement",
            "obj": {
                "bucket": {
                    "name": "test1",
                    "marker": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
                    "bucket_id": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
                    "tenant": "",
                    "explicit_placement": {
                        "data_pool": "",
                        "data_extra_pool": "",
                        "index_pool": ""
                    }
                },
                "key": {
                    "name": "20M.2~uO9gV71ALyIu6DDieeCRzI06zZQ9L1u.1",
                    "instance": "",
                    "ns": "multipart"
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
        "part_ofs": 20971520,
        "stripe_ofs": 20971520,
        "ofs": 20971520,
        "stripe_size": 4194304,
        "cur_part_id": 3,
        "cur_stripe": 0,
        "cur_override_prefix": "",
        "location": {
            "placement_rule": "default-placement",
            "obj": {
                "bucket": {
                    "name": "test1",
                    "marker": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
                    "bucket_id": "d1873e9f-9d2e-40df-81ff-01010c49ae6c.14684.3",
                    "tenant": "",
                    "explicit_placement": {
                        "data_pool": "",
                        "data_extra_pool": "",
                        "index_pool": ""
                    }
                },
                "key": {
                    "name": "20M.2~uO9gV71ALyIu6DDieeCRzI06zZQ9L1u.3",
                    "instance": "",
                    "ns": "multipart"
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
