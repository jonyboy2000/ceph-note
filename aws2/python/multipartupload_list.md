```
import math
from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
url = "http://127.0.0.1:7480"
session = Session(access_key, secret_key)
config = boto3.session.Config(connect_timeout=30000, read_timeout=30000, retries={'max_attempts': 0})
s3_client = session.client('s3', endpoint_url=url, config=config)
src_bucket = "test1"
src_obj = "83M_IA"
dest_bucket = "test1"
dest_obj = "copy"

uploadid = '2~HAw8rseNWgZUgmpgO4JyhLVVTHqBFde'
res = s3_client.list_parts(
    Bucket=dest_bucket,
    Key=dest_obj,
    MaxParts=1000,
    UploadId=uploadid
)

MultipartUpload={
        'Parts': []
    }
for part in res['Parts']:
    MultipartUpload['Parts'].append({'ETag': part['ETag'], 'PartNumber': part['PartNumber']})

print MultipartUpload

# s3_client.complete_multipart_upload(
#     Bucket=dest_bucket,
#     Key=dest_obj,
#     MultipartUpload=MultipartUpload,
#     UploadId=uploadid
# )

s3_client.abort_multipart_upload(
    Bucket=dest_bucket,
    Key=dest_obj,
    UploadId=uploadid
)
```
