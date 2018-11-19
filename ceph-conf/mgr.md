```
./bin/ceph mgr module enable restful -c m1/ceph.conf
./bin/ceph mgr module ls -c m1/ceph.conf
{
    "enabled_modules": [
        "balancer",
        "restful",
        "status"
    ],
    "disabled_modules": [
        "dashboard",
        "influx",
        "localpool",
        "prometheus",
        "selftest",
        "zabbix"
    ]
}

./bin/ceph -c m1/ceph.conf config-key dump -c m1/ceph.conf

{
    "mgr/dashboard/x/server_port": "7791",
    "mgr/restful/keys/admin": "238e5b39-ea56-4bea-9908-abf189f36481",
    "mgr/restful/x/crt": "-----BEGIN CERTIFICATE-----\nMIICyzCCAbMCEEIHdahi0EjZugJ+akZVH4YwDQYJKoZIhvcNAQENBQAwJDELMAkG\nA1UECgwCSVQxFTATBgNVBAMMDGNlcGgtcmVzdGZ1bDAeFw0xODExMTIxMDQzMzFa\nFw0yODExMDkxMDQzMzFaMCQxCzAJBgNVBAoMAklUMRUwEwYDVQQDDAxjZXBoLXJl\nc3RmdWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDMa/DGweBCuuQH\nUAKAXomvu2N+F1Psf+7EDq8R1ndqvFr57CwlgtDYeEoofXXb+UAyA6quSzdiCEaq\n5W6+et2TxPffP4+WSFWImXLPGViuLlhrCoD6Qmfvmi9j7QT4TOs+Oe8QatKxE6qh\nWf7MkCFHF1YgquboDcHCq+L/HgEeDMDfiwRUAle6x3/DyRdEGZKRTq9RS409kya5\nR/ZOqOVdLlh9KHjnpbQ/pDYk4gPtpU0snHiFJyQnX+iSyR5mn4MQtF8tYh+ij6gL\nq65kJbDZi/97tZ6CDp71TeWmEEHWsxcSESVQKsZVXdBB3B3cVf1nNGBGfZkBxhTA\npatkZBJNAgMBAAEwDQYJKoZIhvcNAQENBQADggEBAJKGyttNrY2OffGjhxOI+WOA\nY6/OSQLqGurAlOHTfQaVULf9vX3iNVR7KUjaob8Jea/VNldNA6Tf0D1we+4NGiSm\nftVAg4H6iUo7ZXfGvd5MmjwcC6hgIjfmbrgbIA09itzB5otMWnvo1ZlxiAjr0sMG\n3mRQsxNeqY7Y0+ua9v6DTs2Daqtmn84aYsT+i7XokKLdxAAXOhmemP30pml6su0P\n9Yn5k5RguS+TEFNttDbX5MuGPBrfq4qUDwxCGfd2QLq8JHlf8e8IV6HdZ8hKWaWi\nzwJKoMkDrYHtmdVrld0kBIZqLyCHdEqzF/cm2m120r0pQ4N6sLfnV/nTLzYQ6ME=\n-----END CERTIFICATE-----\n",
    "mgr/restful/x/key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDMa/DGweBCuuQH\nUAKAXomvu2N+F1Psf+7EDq8R1ndqvFr57CwlgtDYeEoofXXb+UAyA6quSzdiCEaq\n5W6+et2TxPffP4+WSFWImXLPGViuLlhrCoD6Qmfvmi9j7QT4TOs+Oe8QatKxE6qh\nWf7MkCFHF1YgquboDcHCq+L/HgEeDMDfiwRUAle6x3/DyRdEGZKRTq9RS409kya5\nR/ZOqOVdLlh9KHjnpbQ/pDYk4gPtpU0snHiFJyQnX+iSyR5mn4MQtF8tYh+ij6gL\nq65kJbDZi/97tZ6CDp71TeWmEEHWsxcSESVQKsZVXdBB3B3cVf1nNGBGfZkBxhTA\npatkZBJNAgMBAAECggEAAt0INGCG2ahwhUGzp0SrvRBs5llBTbDFEW37Oc69QXt9\n8r5CKAxbDI0yzLplKj2ljo3KmEJpdjATfVVVZcmmzOkXZ8MmKb69o/oyR4BdY6M2\njdlJ0TeY6RxJyaaKSUgai3aYSKyWYvCZlUUDcq4aKTrEdBSww1NeAXIS7evnrBoP\nM0PVkeUHAEoM2ir9Ww7xGnluItWZEWkXset/OkmaJrv+f7kMKdfFLhHPgweNtVGt\nkIaqdIH4T6HJyfBUxjH/aoe/UUq/urphxdKDkG/MBHU3EPVXKfdb4uBmStuyUXnc\nbn2Poq+/Le2D0VuqjEQy+1ZhrQxADh5VpFE1nGb7QQKBgQD4j/sXf/U8qK6z6HiQ\nJYfHSpo3JTwxlFNK9reounDDpqrvHNP3d5P9pmsn3/c9kB78e5f648hyAGP9avmD\nTC5rBX5SbmLaXc/jURQoIa29GLBwD+EvDlQUf8n4gKacrLCO1MweDWH4YjqDwekr\ns5eOttWoEQIU2KsqLOEGbij2lQKBgQDSidX3gDl5hLJponhCgTSbeU9ZbEYLEPF3\npKvepmSgyFH8snGKHPw78RGSxpJydjxyqAeQRBwY4umsw/Ftx66NlBbb7vGZodwS\nwTRrOSpM63WgqZ/5Z97Vr/9q1+QExHPHKk8ITqtILy33exLDVAnvp5+xHhQHIBKd\n/GKA0UFW2QKBgEhM4TWhs7zUOBT+vur277rJeXgm7Y5iXaQFhcCfkqNmfHwW/5UR\nBEwYtzyfCfSvUkQQ01FYJnr6oBsbnb5ST4Iz0924XCq2dPzjHaDawwWpA9Fk3RRp\n740S6rXM/im+lZDGVyU6sU+liu2+XsumbqRFjHpZkChuKcOX0FClhGbNAoGAaA9I\nejQeNDmqFRwAZJ6H6fBjj8c8N2wAbSou6LVFN1LLcyKfi6wX32ifTvRmnbxi1CjI\n1D1VxdchuAqA4cm4NLHlOn83Wr/tjjeAOR7gEXSvhuFP+G2mbee3To+2W8TdlKsM\ntQZtEhh/l7p046Y94v3uqBQ9wefQS9XaueCzcsECgYBSA4YZBGBgw6sFmHuPqwsS\nznxM+4Tgi4rYBnGOjvxCWdV+jB0MKD6623VCSa/Ur60AQDUmWG+/sYIPokaiJHNU\nyePbAMo8s6ChQHBeTNYMWgwtUmDwRffaYt6bN7v9MIFBlqhebMdNoImpMlLKJegg\nqA+bCezewJ3r1zmacCFoGA==\n-----END PRIVATE KEY-----\n",
    "mgr/restful/x/server_port": "8791"
}

./bin/ceph config-key set mgr/restful/x/server_port 8791 -c m1/ceph.conf
./bin/ceph config-key set mgr/restful/x/server_addr 127.0.0.1 -c m1/ceph.conf

get_osd.0_info.py

import requests
result = requests.get(
    'https://127.0.0.1:8791/osd/0',
    auth=("admin", "238e5b39-ea56-4bea-9908-abf189f36481"),
    verify=False
)
print result.json()
```

```
# import requests
# from requests_toolbelt.utils import dump
# uri = '/crush/rule'
# uri = '/request?wait=1'
# result = requests.post(
#     'https://ceph-restful:8792'+uri,
#     json={'prefix': 'osd df','output_method':'tree','format':'json'},
# #    json={'prefix': 'osd pool get', 'pool': 'zgp2-z1.rgw.log', 'var':'crush_rule'},
# #    json={'prefix': 'osd pool ls', 'detail': 'true'},
#     auth=("admin", "6d5c0dff-f2d1-4a5d-b610-2ce1556e6703"),
#     verify="/home/onest/ceph/build/s1.crt"
# )
#
# res = result.json()
# # data = dump.dump_all(result)
# # print(data.decode('utf-8'))
# # print res
#
# print res['finished'][0]['outb']



import requests
import json
from requests_toolbelt.utils import dump
uri = '/crush/rule'
uri = '/request?wait=1'
result = requests.post(
    'https://ceph-restful:8792'+uri,
    json={'prefix': 'osd df','output_method':'tree','format':'json'},
#    json={'prefix': 'osd pool get', 'pool': 'zgp2-z1.rgw.log', 'var':'crush_rule'},
#    json={'prefix': 'osd pool ls', 'detail': 'true'},
    auth=("admin", "6d5c0dff-f2d1-4a5d-b610-2ce1556e6703"),
    verify="/home/onest/ceph/build/s1.crt"
)

res = json.loads(result.json()['finished'][0]['outb'])
# data = dump.dump_all(result)
# print(data.decode('utf-8'))
# print res
# print res3


for node in res['nodes']:
    print node['type'], node['name'], node['kb']
#     print i
  # if i['name'] == 'orange' or i['name'] == 'apple':
  #    print i['name'],i['kb']
```
