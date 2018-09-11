```
<?xml version="1.0" encoding="UTF-8" ?>
<workload name="long time read" description="s3 long time read">
    <storage type="s3" config="accesskey=yly;secretkey=yly;endpoint=http://10.254.3.68:8082/" />
    <workflow>
        <workstage name="1">
            <work name="long time read" workers="1" runtime="21600">
                <operation type="read" ratio="100" config="cprefix=test;oprefix=test;containers=c(1);objects=s(1,1000);sizes=c(512)KB" />
            </work>
        </workstage>
    </workflow>
</workload>
```
