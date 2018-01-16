```
# -*- coding: utf-8 -*-

import json
import base64
import os
import oss2
# 以下代码展示了上传回调的用法。
# put_object/complete_multipart_upload支持上传回调，resumable_upload不支持。
# 回调服务器(callbacke server)的示例代码请参考 http://shinenuaa.oss-cn-hangzhou.aliyuncs.com/images/callback_app_server.py.zip
# 您也可以使用OSS提供的回调服务器 http://oss-demo.aliyuncs.com:23450，调试您的程序。调试完成后换成您的回调服务器。

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'testyuliyang')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')
# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param
key = 'quote.txt'
content = "Anything you're good at contributes to happiness."
# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
#
# 准备回调参数，更详细的信息请参考 https://help.aliyun.com/document_detail/31989.html
callback_dict = {}
callback_dict['callbackUrl'] = 'http://67.218.159.42:23450'
# callback_dict['callbackHost'] = 'oss-cn-hangzhou.aliyuncs.com'
callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}'
callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
# 回调参数是json格式，并且base64编码
callback_param = json.dumps(callback_dict).strip()
base64_callback_body = base64.b64encode(callback_param)
print base64_callback_body
# 回调参数编码后放在header中传给oss
headers = {'x-oss-callback': base64_callback_body}

"""
put_object上传回调
"""
# 上传并回调
result = bucket.put_object(key, content, headers)

# 上传并回调成功status为200，上传成功回调失败status为203
assert result.status == 200
# result.resp的内容为回调服务器返回的内容
assert result.resp.read() == '{"Status":"OK"}'

# 确认文件上传成功
result = bucket.head_object(key)
assert result.headers['x-oss-hash-crc64ecma'] == '108247482078852440'

# 删除上传的文件
bucket.delete_object(key)

"""
分片上传回调
"""

# 分片上传回调
# 初始化上传任务
parts = []
upload_id = bucket.init_multipart_upload(key).upload_id
# 上传分片
result = bucket.upload_part(key, upload_id, 1, content)
parts.append(oss2.models.PartInfo(1, result.etag))
# 完成上传并回调
result = bucket.complete_multipart_upload(key, upload_id, parts, headers)

# 上传并回调成功status为200，上传成功回调失败status为203
assert result.status == 200
# result.resp的内容为回调服务器返回的内容
assert result.resp.read() == '{"Status":"OK"}'

# 确认文件上传成功
result = bucket.head_object(key)
assert result.headers['x-oss-hash-crc64ecma'] == '108247482078852440'

# 删除上传的文件
bucket.delete_object(key)
```

表单上传+回调
```
#coding=utf8
import md5
import hashlib
import base64
import hmac
import json
from optparse import OptionParser
def convert_base64(input):
    return base64.b64encode(input)
def get_sign_policy(key, policy):
    return base64.b64encode(hmac.new(key, policy, hashlib.sha1).digest())
def get_form(bucket, endpoint, access_key_id, access_key_secret, out):
    #1 构建一个Post Policy
    policy="{\"expiration\":\"2115-01-27T10:56:19Z\",\"conditions\":[[\"content-length-range\", 0, 1048576],{\"callback\":\"eyJjYWxsYmFja0JvZHlUeXBlIjogImFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIsICJjYWxsYmFja0JvZHkiOiAiZmlsZW5hbWU9JHtvYmplY3R9JnNpemU9JHtzaXplfSZtaW1lVHlwZT0ke21pbWVUeXBlfSIsICJjYWxsYmFja1VybCI6ICJodHRwOi8vNjcuMjE4LjE1OS40MjoyMzQ1MCJ9\"}]}"
    print("policy: %s" % policy)
    #2 将Policy字符串进行base64编码
    base64policy = convert_base64(policy)
    print("base64_encode_policy: %s" % base64policy)
    #3 用OSS的AccessKeySecret对编码后的Policy进行签名
    signature = get_sign_policy(access_key_secret, base64policy)
    #4 构建上传的HTML页面
    form = '''
    <html>
        <meta http-equiv=content-type content="text/html; charset=UTF-8">
        <head><title>OSS表单上传(PostObject)</title></head>
        <body>
            <form  action="http://%s.%s" method="post" enctype="multipart/form-data">
                <input type="text" name="OSSAccessKeyId" value="%s">
                <input type="text" name="policy" value="%s">
                <input type="text" name="Signature" value="%s">
                <input type="text" name="key" value="upload/${filename}">
                <input type="text" name="callback" value="eyJjYWxsYmFja0JvZHlUeXBlIjogImFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIsICJjYWxsYmFja0JvZHkiOiAiZmlsZW5hbWU9JHtvYmplY3R9JnNpemU9JHtzaXplfSZtaW1lVHlwZT0ke21pbWVUeXBlfSIsICJjYWxsYmFja1VybCI6ICJodHRwOi8vNjcuMjE4LjE1OS40MjoyMzQ1MCJ9">        
                <input name="file" type="file" id="file">
                <input name="submit" value="Upload" type="submit">
            </form>
        </body>
    </html>
    ''' % (bucket, endpoint, access_key_id, base64policy, signature)
    f = open(out, "wb")
    f.write(form)
    f.close()
    print("form is saved into %s" % out)
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("", "--bucket", dest="bucket", help="specify ")
    parser.add_option("", "--endpoint", dest="endpoint", help="specify")
    parser.add_option("", "--id", dest="id", help="access_key_id")
    parser.add_option("", "--key", dest="key", help="access_key_secret")
    parser.add_option("", "--out", dest="out", help="out put form")
    (opts, args) = parser.parse_args()
    if opts.bucket and opts.endpoint and opts.id and opts.key and opts.out:
        get_form(opts.bucket, opts.endpoint, opts.id, opts.key, opts.out)
    else:
        print "python %s --bucket=your-bucket --endpoint=oss-cn-hangzhou.aliyuncs.com --id=your-access-key-id --key=your-access-key-secret --out=out-put-form-name" % __file__
```


```
# -*- coding: utf-8 -*-

import json
import base64
import os

import oss2


# 以下代码展示了上传回调的用法。

# put_object/complete_multipart_upload支持上传回调，resumable_upload不支持。
# 回调服务器(callbacke server)的示例代码请参考 http://shinenuaa.oss-cn-hangzhou.aliyuncs.com/images/callback_app_server.py.zip
# 您也可以使用OSS提供的回调服务器 http://oss-demo.aliyuncs.com:23450，调试您的程序。调试完成后换成您的回调服务器。

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'testyuliyang')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')


# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param

key = 'quote.txt'
content = "Anything you're good at contributes to happiness."

# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

#
# 准备回调参数，更详细的信息请参考 https://help.aliyun.com/document_detail/31989.html
callback_dict = {}
callback_dict['callbackUrl'] = 'http://67.218.159.42:23450'
# callback_dict['callbackHost'] = 'oss-cn-hangzhou.aliyuncs.com'
callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}&my_var=${x:var1}'
callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
# 回调参数是json格式，并且base64编码
callback_param = json.dumps(callback_dict).strip()
base64_callback_body = base64.b64encode(callback_param)
# print base64_callback_body
# 回调参数编码后放在header中传给oss
headers = {'x-oss-callback': base64_callback_body}

callback_var = {}
callback_var["x:var1"]='value1'
callback_var["x:var2"]='value2'
callback_var_param = json.dumps(callback_var).strip()
base64_callback_var = base64.b64encode(callback_var_param)
headers['x-oss-callback-var'] = base64_callback_var


"""
put_object上传回调
"""
# 上传并回调
result = bucket.put_object(key, content, headers)

# 上传并回调成功status为200，上传成功回调失败status为203
assert result.status == 200
# result.resp的内容为回调服务器返回的内容
assert result.resp.read() == '{"Status":"OK"}'

# 确认文件上传成功
result = bucket.head_object(key)
assert result.headers['x-oss-hash-crc64ecma'] == '108247482078852440'

# 删除上传的文件
bucket.delete_object(key)

"""
分片上传回调
"""

# 分片上传回调
# 初始化上传任务
# parts = []
# upload_id = bucket.init_multipart_upload(key).upload_id
# # 上传分片
# result = bucket.upload_part(key, upload_id, 1, content)
# parts.append(oss2.models.PartInfo(1, result.etag))
# # 完成上传并回调
# result = bucket.complete_multipart_upload(key, upload_id, parts, headers)
#
# # 上传并回调成功status为200，上传成功回调失败status为203
# assert result.status == 200
# # result.resp的内容为回调服务器返回的内容
# assert result.resp.read() == '{"Status":"OK"}'
#
# # 确认文件上传成功
# result = bucket.head_object(key)
# assert result.headers['x-oss-hash-crc64ecma'] == '108247482078852440'
#
# # 删除上传的文件
# bucket.delete_object(key)
```
