
```
[root@node2 ~]# grep image:  /etc/kubernetes/*.yml &&  grep image:  /etc/kubernetes/manifests/*
/etc/kubernetes/dex-app.yml:      - image: bcpaas/dex-app:1.0
/etc/kubernetes/dex.yml:      - image: quay.io/coreos/dex:v2.0.0
/etc/kubernetes/dnsmasq-autoscaler.yml:        image: gcr.io/google_containers/cluster-proportional-autoscaler-amd64:1.1.1
/etc/kubernetes/dnsmasq-deploy.yml:          image: "andyshinn/dnsmasq:2.72"
/etc/kubernetes/fluent-daemonset.yml:        image: k8s-fluentd:v1.0
/etc/kubernetes/grafana.yml:        image: gcr.io/google_containers/heapster-grafana-amd64:v4.0.2
/etc/kubernetes/heapster.yml:        image: gcr.io/google_containers/heapster-amd64:v1.3.0-beta.1
/etc/kubernetes/influxdb.yml:        image: gcr.io/google_containers/heapster-influxdb-amd64:v1.1.1
/etc/kubernetes/k8s-resource.yml:      - image: k8s-resource:v2.0
/etc/kubernetes/kubedns-autoscaler.yml:        image: gcr.io/google_containers/cluster-proportional-autoscaler-amd64:1.1.1
/etc/kubernetes/kubedns-deploy.yml:        image: "gcr.io/google_containers/kubedns-amd64:1.9"
/etc/kubernetes/kubedns-deploy.yml:        image: "gcr.io/google_containers/kube-dnsmasq-amd64:1.3"
/etc/kubernetes/kubedns-deploy.yml:        image: "gcr.io/google_containers/exechealthz-amd64:1.1"
/etc/kubernetes/kubernetes-dashboard.yml:        image: zounengren/kubernetes-backend:v1.5.5
/etc/kubernetes/kube-state-metrics.yml:#        image: gcr.io/google_containers/kube-state-metrics:v0.3.0
/etc/kubernetes/kube-state-metrics.yml:        image: batazor/kube-state-metrics:0.4.1
/etc/kubernetes/ldap.yml:          image: osixia/openldap:1.1.8
/etc/kubernetes/mysql.yml:      - image: mysql:5.6
/etc/kubernetes/node-exporter.yml:      - image: prom/node-exporter:latest
/etc/kubernetes/paas-auth.yml:      - image: bcpaas/paas-auth:1.0
/etc/kubernetes/redis.yml:      - image: redis
/etc/kubernetes/manifests/kube-apiserver.manifest:    image: quay.io/coreos/hyperkube:v1.6.4_coreos.0
/etc/kubernetes/manifests/kube-controller-manager.manifest:    image: quay.io/coreos/hyperkube:v1.6.4_coreos.0
/etc/kubernetes/manifests/kube-proxy.manifest:    image: quay.io/coreos/hyperkube:v1.6.4_coreos.0
/etc/kubernetes/manifests/kube-scheduler.manifest:    image: quay.io/coreos/hyperkube:v1.6.4_coreos.0

```
