# -*- coding: utf-8 -*-
import base64
import random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

# aes 256, key always is 32 bytes
_AES_256_KEY_SIZE = 32
_AES_CTR_COUNTER_BITS_LEN = 8 * 16
class AESCipher:
    def __init__(self, key=None, start=None):
        self.key = key
        self.start = start
        if not self.key:
            self.key = Random.new().read(_AES_256_KEY_SIZE)
        if not self.start:
            self.start = random.randint(1, 10)
        ctr = Counter.new(_AES_CTR_COUNTER_BITS_LEN, initial_value=self.start)
        self.cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
    def encrypt(self, raw):
        return self.cipher.encrypt(raw)
    def decrypt(self, enc):
        return self.cipher.decrypt(enc)

# 0.1 生成rsa key文件并保存到disk
rsa_private_key_obj = RSA.generate(2048)
rsa_public_key_obj = rsa_private_key_obj.publickey()
encrypt_obj = PKCS1_OAEP.new(rsa_public_key_obj)
decrypt_obj = PKCS1_OAEP.new(rsa_private_key_obj)
# save to local disk
file_out = open("private_key.pem", "w")
file_out.write(rsa_private_key_obj.exportKey())
file_out.close()
file_out = open("public_key.pem", "w")
file_out.write(rsa_public_key_obj.exportKey())
file_out.close()

#### 1 Put Object  ####
# 1.1 生成加密这个object所用的一次性的对称密钥 encrypt_cipher, 其中的key 和 start为随机生成的value
encrypt_cipher = AESCipher()

from boto3.session import Session
import boto3
access_key = "yly"
secret_key = "yly"
url = "http://10.139.12.23"
session = Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
s3 = session.client('s3', endpoint_url=url)

content = "hello world"
# 1.2. 用 encrypt_cipher 对原始content加密得到encrypt_content
encryt_content = encrypt_cipher.encrypt(content)

# 1.3 将辅助解密的信息用公钥加密后存到object的自定义meta中. 后续当我们get object时，就可以根据自定义meta，用私钥解密得到原始content
s3.put_object(Bucket="iosonesttest",Key= 'xxxxx',
              Metadata={
                  'x-amx-meta-x-amx-key': base64.b64encode(encrypt_obj.encrypt(encrypt_cipher.key)),
                  'x-amx-meta-x-amx-start': base64.b64encode(encrypt_obj.encrypt(str(encrypt_cipher.start)))},
              Body=encryt_content)

# 2.1 下载得到加密后的object
resp = s3.get_object(Bucket="iosonesttest", Key="xxxxx")
download_encrypt_content=''
with open('local-backup.bin','wb') as f:
    download_encrypt_content = resp['Body'].read()

# 2.2 从自定义meta中解析出之前加密这个object所用的key 和 start 
download_encrypt_key = base64.b64decode(resp['Metadata']['x-amx-meta-x-amx-key'])
key = decrypt_obj.decrypt(download_encrypt_key)
download_encrypt_start = base64.b64decode(resp['Metadata']['x-amx-meta-x-amx-start'])
start = int(decrypt_obj.decrypt(download_encrypt_start))

# 2.3 生成解密用的cipher, 并解密得到原始content
decrypt_cipher = AESCipher(key, start)

download_content = decrypt_cipher.decrypt(download_encrypt_content)
print download_content
