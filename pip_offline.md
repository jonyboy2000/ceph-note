离线安装pip包

```
virtualenv vir/
proxychains python setup.py install 
pip freeze > requirements.txt

boto3==1.5.22
botocore==1.8.36
certifi==2018.1.18
chardet==3.0.4
crcmod==1.7
docutils==0.14
futures==3.2.0
idna==2.6
jmespath==0.9.3
oss2==2.4.0
python-dateutil==2.6.1
requests==2.18.4
s3transfer==0.1.12
six==1.11.0
urllib3==1.22

mkdir $HOME/.mypypi
proxychains pip install --download $HOME/.mypypi -r requirements.txt
pip install --no-index --find-links /$HOME/.mypypi -r requirements.txt
```
