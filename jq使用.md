

```
#顺序删除channel
./livestream.sh -c tdk112701.cfg list |jq '.channels[]' | awk -F"\"" '{print $1 $2}' | awk -F"/" '{ system("./livestream.sh -c tdk112701.cfg delete "  $1 " " $2)}'

#100并发删除channel
./livestream.sh -c tdk112701.cfg list |jq '.channels[]' | awk -F"\"" '{print $1 $2}' | awk -F"/" '{ print "./livestream.sh -c tdk112701.cfg delete "  $1 " " $2}' | xargs -I{} -P 100  sh -c {}
```

列出桶下对象
```
radosgw-admin bi list --bucket=aws4c | jq .[] |jq .entry.name
```
