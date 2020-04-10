### Configuration
copy config.yml.example to config.yml and change router_* variables
```yaml
comment_for_routing: "office-vpn"
network_hash_file: "/tmp/networks_hash"
router_ip: '192.168.88.1'
router_user: 'admin'
router_password: '****'
gateway: "office"
hosts:
  - google.com:
    - account #this will be subdomains account.google.com
  - habr.com:
```
**gateway** - this you vpn connection or you can use any ip that can route you to destination hosts

### Install requirements
```bash
pip3 install -r requirements.txt
```
Needed  PyYAML 5.1 and later.

### Running
You can simply put this script to cron if yours ips dynamic
```bash
python3 mikrotik.py
```
