
```
import com.amazonaws.ClientConfiguration;
import com.amazonaws.HttpMethod;
import com.amazonaws.Protocol;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.retry.PredefinedRetryPolicies;
import com.amazonaws.retry.RetryPolicy;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.S3ClientOptions;
import com.amazonaws.services.s3.model.*;

import java.io.*;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;


public class S3Sample {
    private static Logger logger = Logger.getLogger(S3Sample.class);
    private static final String ACCESS_KEY = "";
    private static final String SECRET_KEY = "";
    private static final String ENDPOINT = "http://eos-beijing-1.cmecloud.cn";

    public static void main(String[] args) throws IOException {
        AWSCredentials credentials = new BasicAWSCredentials(ACCESS_KEY, SECRET_KEY);
        ClientConfiguration opts = new ClientConfiguration();

//        opts.setSignerOverride("S3SignerType");
        opts.setSignerOverride("AWSS3V4SignerType");
        opts.setProtocol(Protocol.HTTP);
        opts.setRetryPolicy(PredefinedRetryPolicies.NO_RETRY_POLICY);
        AmazonS3 s3 = new AmazonS3Client(credentials, opts);
        s3.setEndpoint(ENDPOINT);
        s3.setS3ClientOptions(new S3ClientOptions().withPathStyleAccess(true));

        String bucketname = "cosbench-test2";
        bucketname = "testversionsbeijing1";

//        String keyMarker = "500wks_16KB42948";
//        ListObjectsRequest request = new ListObjectsRequest();
//        request.withBucketName(bucketname).withMarker(keyMarker);
//        ObjectListing objects = s3.listObjects(request);
//        for (S3ObjectSummary s3ObjectSummary: objects.getObjectSummaries()) {
//            System.out.println(s3ObjectSummary.getKey());
//        }


//        String nextMarker = null;
//        ObjectListing objects;
//        do {
//            ListObjectsRequest request = new ListObjectsRequest();
//            request.withBucketName(bucketname).withMarker(nextMarker);
//            objects  = s3.listObjects(request);
//            for (S3ObjectSummary s3ObjectSummary: objects.getObjectSummaries()) {
//                System.out.println(s3ObjectSummary.getKey());
//            }
//            nextMarker = objects.getNextMarker();
//        } while (objects.isTruncated());

        ListVersionsRequest listVersionsRequest = new ListVersionsRequest();
        listVersionsRequest.setBucketName(bucketname);
        listVersionsRequest.withKeyMarker("aopalliance-1.0-8.el7.noarch.rpm");
        listVersionsRequest.withVersionIdMarker("f89NOJjNDbR3sL16.VJy1rtIFV-Ewvh");
        VersionListing versionListing = s3.listVersions(listVersionsRequest);
        List<String> versionIds = new ArrayList<String>();
        int maxnum = 1;
        String lastkey = "";
        String lastkey_versionid = "";
        do {
            for (S3VersionSummary s3VersionSummary : versionListing.getVersionSummaries()) {
                System.out.println(s3VersionSummary.getKey() + " versionid= " + s3VersionSummary.getVersionId());
                maxnum ++;
                if (maxnum > 10) {
                    lastkey = s3VersionSummary.getKey();
                    lastkey_versionid = s3VersionSummary.getVersionId();
                    break;
                }
            }
            versionListing = s3.listNextBatchOfVersions(versionListing);
        }
        while (versionListing.isTruncated());

        System.out.println("the last key and version id");
        System.out.println(lastkey);
        System.out.println(lastkey_versionid);

    }
}

```
