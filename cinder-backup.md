driver目录
```
[root@ceph04 yuliyang]# cd /usr/lib/python2.7/site-packages/cinder/backup/drivers/
[root@ceph04 drivers]# ls -l
total 352
-rw-r--r-- 1 root root 49688 Nov 17 02:21 ceph.py
-rw-r--r-- 2 root root 38859 Nov 17 02:30 ceph.pyc
-rw-r--r-- 2 root root 38859 Nov 17 02:30 ceph.pyo
-rw-r--r-- 1 root root  3480 Nov 17 02:21 glusterfs.py
-rw-r--r-- 2 root root  3400 Nov 17 02:30 glusterfs.pyc
-rw-r--r-- 2 root root  3400 Nov 17 02:30 glusterfs.pyo
-rw-r--r-- 1 root root 14327 Nov 17 02:21 google.py
-rw-r--r-- 2 root root 14878 Nov 17 02:30 google.pyc
-rw-r--r-- 2 root root 14878 Nov 17 02:30 google.pyo
-rw-r--r-- 1 root root     0 Nov 17 02:21 __init__.py
-rw-r--r-- 2 root root   153 Nov 17 02:30 __init__.pyc
-rw-r--r-- 2 root root   153 Nov 17 02:30 __init__.pyo
-rw-r--r-- 1 root root  3107 Nov 17 02:21 nfs.py
-rw-r--r-- 2 root root  3106 Nov 17 02:30 nfs.pyc
-rw-r--r-- 2 root root  3106 Nov 17 02:30 nfs.pyo
-rw-r--r-- 1 root root  5416 Nov 17 02:21 posix.py
-rw-r--r-- 2 root root  5389 Nov 17 02:30 posix.pyc
-rw-r--r-- 2 root root  5389 Nov 17 02:30 posix.pyo
-rw-r--r-- 1 root root 17026 Nov 17 02:21 swift.py
-rw-r--r-- 2 root root 14834 Nov 17 02:30 swift.pyc
-rw-r--r-- 2 root root 14834 Nov 17 02:30 swift.pyo
-rw-r--r-- 1 root root 20882 Nov 17 02:21 tsm.py
-rw-r--r-- 2 root root 16417 Nov 17 02:30 tsm.pyc
-rw-r--r-- 2 root root 16417 Nov 17 02:30 tsm.pyo

```
list and delete
```
[onest@ceph04 yuliyang]$ cinder backup-list
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| ID                                   | Volume ID                            | Status    | Name | Size | Object Count | Container     |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
| 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 | ef3a93f7-c57b-4834-9f0e-6482fa9e1296 | available | -    | 1    | 22           | volumebackups |
+--------------------------------------+--------------------------------------+-----------+------+------+--------------+---------------+
[onest@ceph04 yuliyang]$ cinder backup-delete 461b51c1-7c9e-4c41-9f03-23cba4c0ef23
Request to delete backup 461b51c1-7c9e-4c41-9f03-23cba4c0ef23 has been accepted.
[onest@ceph04 yuliyang]$ cinder backup-list
+----+-----------+--------+------+------+--------------+-----------+
| ID | Volume ID | Status | Name | Size | Object Count | Container |
+----+-----------+--------+------+------+--------------+-----------+
+----+-----------+--------+------+------+--------------+-----------+

```
