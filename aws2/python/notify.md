# 获取桶通知
```
from boto3.session import Session

#import os
#os.environ['HTTP_PROXY'] = 'http://192.168.153.1:7777'

import json
import boto3
access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)
s3_client = session.client('s3', endpoint_url=url )
conf = s3_client.get_bucket_notification_configuration(Bucket="***")
print json.dumps(conf['TopicConfigurations'], indent=4, sort_keys=True)
```
# 设置桶通知
```
from boto3.session import Session
import json
import boto3
access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)

AVAILABLE_CONFIGURATIONS = (
    'LambdaFunctionConfigurations', #LAMBADA
    'TopicConfigurations',          #SNS
    'QueueConfigurations'           #SQS
)

bucket_notifications_config = {
'TopicConfigurations' : [
        {
            "Events": [
                "s3:ObjectCreated:*"
            ],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {
                            "Name": "Suffix",
                            "Value": ".jpg"
                        }
                    ]
                }
            },
            "Id": "image",
            "TopicArn": "arn:aws:sns:us-east-1:***:image"
        },
        {
            "Events": [
                "s3:ObjectCreated:*"
            ],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {
                            "Name": "Suffix",
                            "Value": ".txt"
                        }
                    ]
                }
            },
            "Id": "png",
            "TopicArn": "arn:aws:sns:us-east-1:***:image"
        }
    ]
}
s3_client = session.client('s3', endpoint_url=url )
print s3_client.put_bucket_notification_configuration(Bucket="***", NotificationConfiguration=bucket_notifications_config)
```
# 清除桶通知（无法delete, method not allowed）
```
from boto3.session import Session
import json
import boto3
access_key = ""
secret_key = ""
url = "http://s3.amazonaws.com"
session = Session(access_key, secret_key)
bucket_notifications_config = {
'TopicConfigurations' : [
    ]
}
s3_client = session.client('s3', endpoint_url=url )
print s3_client.put_bucket_notification_configuration(Bucket="***", NotificationConfiguration=bucket_notifications_config)
```
