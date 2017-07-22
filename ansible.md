远端A机器生成，所有其他机器读取
```
---
- name: create monitor initial keyring
  copy: content="genarate by hosts " dest=/tmp/hello.txt
  run_once: true
  delegate_to:  "{{ groups['test'][0] }}"

- name: fetch contents of mon_secret file
  slurp: path=/tmp/hello.txt
  run_once: true
  delegate_to: "{{ groups['test'][0] }}"
  register: mon_secret_file

- debug: msg="{{ mon_secret_file['content'] | b64decode }}"


#copy large file
yum install -y sshpass rsync
local_action: "shell rsync -avz -e 'sshpass -p {{ ansible_ssh_pass }} ssh -p 22' {{ role_path }}/files/quay.io_coreos_dex_v2.0.0.tar {{ ansible_ssh_user }}@{{hostvars[groups['user_management'][0]]['ip']}}:{{paas_images_dir}}/quay.io_coreos_dex_v2.0.0.tar"
```

