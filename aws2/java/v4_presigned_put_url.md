aws4

```
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.ClientConfiguration;
import com.amazonaws.HttpMethod;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.*;
import com.amazonaws.util.StringUtils;

import java.io.*;
import java.util.List;
import java.util.UUID;

/**
 * This sample demonstrates how to make basic requests to Amazon S3 using the
 * AWS SDK for Java.
 * <p>
 * <b>Prerequisites:</b> You must have a valid Amazon Web Services developer
 * account, and be signed up to use Amazon S3. For more information on Amazon
 * S3, see http://aws.amazon.com/s3.
 * <p>
 * Fill in your AWS access credentials in the provided credentials file
 * template, and be sure to move the file to the default location
 * (~/.aws/credentials) where the sample code will load the credentials from.
 * <p>
 * <b>WARNING:</b> To avoid accidental leakage of your credentials, DO NOT keep
 * the credentials file in your source directory.
 *
 * http://aws.amazon.com/security-credentials
 */
public class S3Sample {

    private static final String ACCESS_KEY = "accesskey";
    private static final String SECRET_KEY = "secretkey";
    private static final String ENDPOINT = "http://eos-beijing-2.cmecloud.cn";

    public static void main(String[] args) throws IOException {

        AWSCredentials credentials = new BasicAWSCredentials(ACCESS_KEY, SECRET_KEY);
        ClientConfiguration opts = new ClientConfiguration();
//        opts.setSignerOverride("S3SignerType");     //v2
        opts.setSignerOverride("AWSS3V4SignerType");  //v4
        AmazonS3 s3 = new AmazonS3Client(credentials, opts);
        s3.setEndpoint(ENDPOINT);

        java.util.Date expiration = new java.util.Date();
        long milliSeconds = expiration.getTime();
        milliSeconds += 1000 * 60 * 60; // Add 1 hour.
        expiration.setTime(milliSeconds);

        GeneratePresignedUrlRequest request = new GeneratePresignedUrlRequest("beijing2-bucket", "1.txt");
        request.setMethod(HttpMethod.PUT);
        request.setExpiration(expiration);
        System.out.println(s3.generatePresignedUrl(request));

    }
}




export URL="http://beijing2-bucket.eos-beijing-2.cmecloud.cn/1.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20180104T045843Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3599&X-Amz-Credential=ZY31KLNTI15OJ8GNNOZM%2F20180104%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=03b0ac45828f8d75862d2d5bb3fa797e2dbd6b7c6e74c0b24c14bbc604d6d0f1"
echo abcde > test.txt
curl -D - -X PUT --upload-file test.txt $URL -H "Host:beijing2-bucket.eos-beijing-2.cmecloud.cn"
```
