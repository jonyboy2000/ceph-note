
环境安装
```
proxychains yum install mono-devel
#proxychains git clone https://github.com/aws/aws-sdk-net.git
proxychains yum install nuget
proxychains nuget install AWSSDK

nuget config -set http_proxy=http://192.168.153.1:7777
nuget install  AWSSDK.S3 -Version 3.3.16.2

#export MONO_PATH=`pwd`/AWSSDK.2.3.55.2/lib/net35:.

export MONO_PATH=`pwd`/AWSSDK.S3.3.3.16.2/lib/net35/:.
```
vi s3.cs
```
using System;
using Amazon.S3;
using Amazon.S3.Model;

class Upload
{
  public static void Main(string[] args)
  {
    Amazon.S3.AmazonS3Config clientConfig  = new Amazon.S3.AmazonS3Config()
    {
        ServiceURL = "http://10.139.12.23",
        ForcePathStyle = true,
        SignatureMethod = Amazon.Runtime.SigningAlgorithm.HmacSHA256,
        SignatureVersion = "s3v2",
        MaxErrorRetry = 1
    };
    AmazonS3Client client = new AmazonS3Client("yly","yly",clientConfig);
    PutObjectRequest request = new PutObjectRequest
    {
      BucketName = "public",
      Key = "Item1",
      ContentBody = "This is sample content..."
    };
    client.PutObject(request);
    }
}
```
编译
```
mcs s3.cs -r:./AWSSDK.2.3.55.2/lib/net35/AWSSDK.dll

[root@promote test]# ls -l
total 12
drwxr-xr-x. 4 root root   56 Dec 28 05:54 AWSSDK.2.3.55.2
drwxr-xr-x. 9 root root 4096 Dec 28 05:47 aws-sdk-net
drwxr-xr-x. 4 root root   87 Dec 28 05:54 Microsoft.Bcl.1.1.7
drwxr-xr-x. 4 root root   96 Dec 28 05:54 Microsoft.Bcl.Build.1.0.14
drwxr-xr-x. 3 root root   95 Dec 28 05:54 Microsoft.Net.Http.2.1.10
-rw-r--r--. 1 root root  769 Dec 28 06:20 s3.cs
-rwxr-xr-x. 1 root root 3584 Dec 28 06:20 s3.exe  <==编译后生成

```

运行
```
mono s3.exe
```


list 桶列表
```
using System;
using Amazon.S3;
using Amazon.S3.Model;

class Upload
{
  public static void Main(string[] args)
  {
    // Create a client

    Amazon.S3.AmazonS3Config clientConfig  = new Amazon.S3.AmazonS3Config()
    {
        ServiceURL = "http://eos-beijing-1.cmecloud.cn",
        ForcePathStyle = true,
        SignatureMethod = Amazon.Runtime.SigningAlgorithm.HmacSHA256,
        SignatureVersion = "s3v2",
        MaxErrorRetry = 1
    };

    AmazonS3Client client = new AmazonS3Client("xx","yy",clientConfig);

    ListBucketsResponse response = client.ListBuckets();
    foreach (S3Bucket b in response.Buckets)
      {
        Console.WriteLine("{0}\t{1}", b.BucketName, b.CreationDate);
      }
    }
}
```

获取桶的location
```

using System;
using Amazon.S3;
using Amazon.S3.Model;

class Upload
{
  public static void Main(string[] args)
  {
    // Create a client

    Amazon.S3.AmazonS3Config clientConfig  = new Amazon.S3.AmazonS3Config()
    {
        ServiceURL = "http://eos-beijing-1.cmecloud.cn",
        ForcePathStyle = true,
        SignatureMethod = Amazon.Runtime.SigningAlgorithm.HmacSHA256,
        SignatureVersion = "s3v2",
        MaxErrorRetry = 1
    };

    AmazonS3Client client = new AmazonS3Client("xxxx","yyyy",clientConfig);

    var request = new GetBucketLocationRequest()
    {
                BucketName = "ylybeijing1"
    };
    var response = client.GetBucketLocation(request);
    Console.WriteLine(response.Location.ToString());

    }
}

```
