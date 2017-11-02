#phpstorm调试
```
yum install php-pecl-xdebug
```
#demo
```
<?php
require_once 'AWSSDKforPHP/sdk.class.php';
define('AWS_KEY', 'onest');
define('AWS_SECRET_KEY', 'onest');
define('AWS_CANONICAL_ID', 'hshao_uid');
define('AWS_CANONICAL_NAME', 'hshao');
define('HOST', '10.139.13.205');
if (!extension_loaded('curl') && !@dl(PHP_SHLIB_SUFFIX == 'so' ? 'curl.so' : 'php_curl.dll')) {
    exit("ERROR: CURL extension not loaded");
}
$credentials = array(
    'key'    => AWS_KEY,
    'secret' => AWS_SECRET_KEY,
    'default_cache_config' => '',
    'certificate_authority' => false,
    '@default' => 'development'

);

$Connection = new AmazonS3($credentials);
$Connection->disable_ssl();
//$Connection->disable_ssl_verification();
$Connection->enable_path_style(false);
$Connection->set_hostname(HOST);
$Connection->allow_hostname_override(false);
$bucket = 'test1';
$region = AmazonS3::REGION_US_E1;
$Connection->set_vhost(HOST . '/' . $bucket);
//$res = $Connection->set_bucket_acl($bucket,AmazonS3::ACL_PUBLIC);
//$res = $Connection->enable_versioning($bucket);
//$res = $Connection->disable_versioning($bucket);
//var_dump($res);


//$ObjectsListResponse = $Connection->list_objects($bucket);
//$Objects = $ObjectsListResponse->body->Contents;
//foreach ($Objects as $Object) {
//    echo $Object->Key . "\t" . $Object->Size . "\t" . $Object->LastModified . "\n";
//}


$res = $Connection->get_bucket_region("test1");
var_dump($res);
//var_dump($res['body']);
//$ListResponse = $Connection->list_buckets();
//$Buckets = $ListResponse->body->Buckets->Bucket;
//foreach ($Buckets as $Bucket) {
//    echo $Bucket->Name . "\t" . $Bucket->CreationDate . "\n";
//}
```
