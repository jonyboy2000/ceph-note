
```
#安装
pip install awscli
#配置
aws configure
#使用v2认证
aws configure set default.s3.signature_version s3
#使用v4认证
aws configure set default.s3.signature_version s3v4
#列出桶列表
aws --endpoint-url http://127.0.0.1:8000 s3 ls
#创建桶
aws --endpoint-url http://127.0.0.1:8000 s3 mb s3://newbucket
#上传对象
aws --endpoint-url http://127.0.0.1:8000 s3 cp yly.s3cfg  s3://newbucket
#删除对象
aws --endpoint-url http://127.0.0.1:8000 s3 rm s3://newbucket/yly.s3cfg
aws --endpoint-url http://127.0.0.1:8000 s3 rm s3://czfyybf20171109 --recursive
#删除桶
aws --endpoint-url http://127.0.0.1:8000 s3 rb s3://ylybucket
```
