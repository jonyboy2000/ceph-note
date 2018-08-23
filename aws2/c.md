
调试libs3
```
DEBUG=true make install

cmake_minimum_required(VERSION 3.7.1)
project(untitled6 C)
set(CMAKE_C_STANDARD 99)
add_executable(untitled6 main.c)
target_link_libraries(untitled6 libs3.a xml2 z m dl curl pthread)
```





```
#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include "libs3.h"
#include <sys/stat.h>

//yum install libs3 libs3-devel
//https://github.com/fabian4/document/tree/master/object_storage/development/sdk/cpp
//target_link_libraries(untitled6 s3 xml2 z m dl curl pthread)

typedef struct put_object_callback_data
{
  FILE *infile;
  uint64_t contentLength;
} put_object_callback_data;

static int putObjectDataCallback(int bufferSize, char *buffer, void *callbackData)
{
  put_object_callback_data *data = (put_object_callback_data *) callbackData;
  int ret = 0;
  if (data->contentLength) {
    int toRead = ((data->contentLength > (unsigned) bufferSize) ? (unsigned) bufferSize : data->contentLength);
    ret = fread(buffer, 1, toRead, data->infile);
  }
  data->contentLength -= ret;
  return ret;
}

S3Status responsePropertiesCallback(const S3ResponseProperties *properties, void *callbackData) {
  return S3StatusOK;
}

static void responseCompleteCallback(S3Status status, const S3ErrorDetails *error, void *callbackData) {
  return;
}

int main(int argc, char *argv[])
{
  S3_initialize("s3", S3_INIT_ALL, "10.254.3.68");

  put_object_callback_data data;
  const char sample_file[] = "/root/libs3-2.0/TODO";
  const char sample_key[] = "test2/index.m3u8";
  struct stat statbuf;
  if (stat(sample_file, &statbuf) == -1) {
    fprintf(stderr, "\nERROR: Failed to stat file %s: ", sample_file);
    perror(0);
  }

  int contentLength = statbuf.st_size;
  data.contentLength = contentLength;

  if (!(data.infile = fopen(sample_file, "r"))) {
    fprintf(stderr, "\nERROR: Failed to open input file %s: ", sample_file);
    perror(0);
  }

  S3ResponseHandler responseHandler =
    {
      &responsePropertiesCallback,
      &responseCompleteCallback
    };

  S3PutObjectHandler putObjectHandler =
    {
      responseHandler,
      &putObjectDataCallback
    };

  S3BucketContext bucketContext =
    {
      "10.254.3.68",
      "libs3",
      S3ProtocolHTTP,
      S3UriStylePath,
      "yly",
      "yly"
    };
    
  const char *cacheControl = 0, *contentType = 0, *md5 = 0;
  const char *contentDispositionFilename = 0, *contentEncoding = 0;
  int64_t expires = -1;
  S3CannedAcl cannedAcl = S3CannedAclBucketOwnerFullControl;
  int metaPropertiesCount = 2;
  S3NameValue metaProperties[S3_MAX_METADATA_COUNT];
  S3NameValue prop1, prop2;
  prop1.name = "color";
  prop1.value = "red";
  prop2.name = "country";
  prop2.value = "USA";
  metaProperties[0] = prop1;
  metaProperties[1] = prop2;
  char useServerSideEncryption = 0;
  S3PutProperties putProperties =
    {
      contentType,
      md5,
      cacheControl,
      contentDispositionFilename,
      contentEncoding,
      expires,
      cannedAcl,
      metaPropertiesCount,
      metaProperties,
      useServerSideEncryption
    };

  S3_put_object(&bucketContext, sample_key, contentLength, &putProperties, NULL,
                &putObjectHandler, &data);

  S3_deinitialize();
  return 0;
}
```
