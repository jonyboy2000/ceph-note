
## create bucket and set cors
```
s3cmd mb s3://ylybucket
s3cmd setcors cors.xml s3://ylybucket
```
## cors.xml
```
<?xml version="1.0"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedHeader>*</AllowedHeader>
    <ExposeHeader>ETag</ExposeHeader>
  </CORSRule>
</CORSConfiguration>
```

upload.html
```
<!DOCTYPE html>
<html>
  <head>
    <script src="https://sdk.amazonaws.com/js/aws-sdk-2.100.0.min.js"></script>
  </head>
  <body>
    <h1>App</h1>
    <input type="file" id="file-chooser" />
    <button id="upload-button">Upload to S3</button>
    <div id="results"></div>
  </body>
<script type="text/javascript">
    var s3 = new AWS.S3({
    apiVersion: '2006-03-01',
    accessKeyId: "yly",
    secretAccessKey: "yly",
    endpoint: "http://10.254.3.68",
    s3ForcePathStyle: true,
    signatureVersion: 'v2',
    sslEnabled: true
    });
    var fileChooser = document.getElementById('file-chooser');
    var button = document.getElementById('upload-button');
    var results = document.getElementById('results');
    button.addEventListener('click', function() {
    var file = fileChooser.files[0];
    if (file) {
      results.innerHTML = '';
      var params = {Key: file.name,Bucket: "ylybucket", ContentType: file.type, Body: file};
      s3.putObject(params, function (err, data) {
        results.innerHTML = err ? 'ERROR!' : 'UPLOADED.';
      });
    } else {
      results.innerHTML = 'Nothing to upload.';
    }
    }, false);
</script>
</html>
```

