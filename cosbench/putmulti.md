```
<?xml version="1.0" encoding="UTF-8" ?>
<workload name="long time" description="s3 long time">
    <workflow>
        <workstage name="1">
            <work name="long time" workers="100" totalOps="100000">
				<storage type="s3" config="accesskey=yly;secretkey=yly;endpoint=http://10.63.33.1:8083/" />
                <operation type="write" ratio="100" config="cprefix=testbl;oprefix=test;containers=c(2);objects=s(1,100000);sizes=c(512)KB" />
            </work>
			<work name="long time" workers="100" totalOps="100000">
				<storage type="s3" config="accesskey=yly;secretkey=yly;endpoint=http://10.63.33.3:8083/" />
                <operation type="write" ratio="100" config="cprefix=testbl;oprefix=test;containers=c(2);objects=s(100001,200000);sizes=c(512)KB" />
            </work>
			<work name="long time" workers="100" totalOps="100000">
				<storage type="s3" config="accesskey=yly;secretkey=yly;endpoint=http://10.63.33.4:8083/" />
                <operation type="write" ratio="100" config="cprefix=testbl;oprefix=test;containers=c(2);objects=s(200001,300000);sizes=c(512)KB" />
            </work>
        </workstage>
    </workflow>
</workload>
```
