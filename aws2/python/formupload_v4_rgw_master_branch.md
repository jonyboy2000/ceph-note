```
#!/usr/bin/python
from boto3.session import Session
import boto3
BUCKET = 'test222'
KEY    = 'test-1-2-1-key'
TEST_FILE = 'test-rgw-s3-aws4-form.html'
access_key = "yly3"
secret_key = "yly3"
url = "http://192.168.153.177:8000" 
session = Session(access_key, secret_key)
s3_client = session.client(
    's3',
    endpoint_url=url,
    use_ssl = False,
    config = boto3.session.Config(
         signature_version = 's3v4',   #v2的话 signature_version = 's3',
	 addressing_style = 'path' #virtual
    )
)
conditions = [
    ["content-length-range", 10, 1000000000]
]

form_data = s3_client.generate_presigned_post(
    Conditions = conditions,
    Bucket = BUCKET,
    Key = KEY
)

#use request to simulate brower post upload
#files = {"file": "file_content"}
#response = requests.post(form_data["url"], data=form_data["fields"], files=files)

html = """\
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
      <form action="{url}" method="post" enctype="multipart/form-data">
""".format(url=form_data['url'])

for k, v in form_data['fields'].items():
	html += """
           <input type="hidden" name="{key}" value="{value}" />
        """.format(key=k,value=v)

html += """
      File:
      <input type="file"   name="file" /> <br />
    <input type="submit" name="submit" value="Upload to Amazon S3" />
  </form>
</html>
"""

file = open(TEST_FILE, "w")
file.write(html)
file.close()

print TEST_FILE + " created."

```

output html file and open in brower:
```

<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
      <form action="http://192.168.153.177:8000/test222" method="post" enctype="multipart/form-data">

           <input type="hidden" name="x-amz-algorithm" value="AWS4-HMAC-SHA256" />
        
           <input type="hidden" name="key" value="test-1-2-1-key" />
        
           <input type="hidden" name="x-amz-signature" value="442a054b5590c41dfc8df2eddc32372b25c16ab25ca690f2b3e9ae8b7b6c90c8" />
        
           <input type="hidden" name="x-amz-date" value="20180109T081316Z" />
        
           <input type="hidden" name="policy" value="eyJjb25kaXRpb25zIjogW1siY29udGVudC1sZW5ndGgtcmFuZ2UiLCAxMCwgMTAwMDAwMDAwMF0sIHsiYnVja2V0IjogInRlc3QyMjIifSwgeyJrZXkiOiAidGVzdC0xLTItMS1rZXkifSwgeyJ4LWFtei1hbGdvcml0aG0iOiAiQVdTNC1ITUFDLVNIQTI1NiJ9LCB7IngtYW16LWNyZWRlbnRpYWwiOiAieWx5My8yMDE4MDEwOS91cy1lYXN0LTEvczMvYXdzNF9yZXF1ZXN0In0sIHsieC1hbXotZGF0ZSI6ICIyMDE4MDEwOVQwODEzMTZaIn1dLCAiZXhwaXJhdGlvbiI6ICIyMDE4LTAxLTA5VDA5OjEzOjE2WiJ9" />
        
           <input type="hidden" name="x-amz-credential" value="yly3/20180109/us-east-1/s3/aws4_request" />
        
      File:
      <input type="file"   name="file" /> <br />
    <input type="submit" name="submit" value="Upload to Amazon S3" />
  </form>
</html>
```
