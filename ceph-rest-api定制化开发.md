
/usr/lib/python2.7/site-packages/ceph_rest_api.py

```
import json
resp = json.loads(open('df.json','rb').read())
for node in resp[u'output'][u'nodes']:
    if node[u'type'] == 'root':
        print node
        if node['name'] == 'orange':
            print node['kb_used']
            node['kb_used'] = int(node['kb_used'] * 2 / 3)
            node['kb_avail'] = int(node['kb_avail'] * 2 / 3 * 0.9)
        if node['name'] == 'apple':
            node['kb_used'] = int(node['kb_used'] / 3)
            node['kb_avail'] = int(node['kb_avail'] / 3 * 0.9)
        print node

for node in resp[u'output'][u'nodes']:
    if node[u'type'] == 'root':
        print node
```
