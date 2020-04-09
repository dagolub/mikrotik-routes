import os
import routeros_api
import socket
from datetime import datetime
from config import cfg


class MikrotikVpnManager:
    def __init__(self):
        self.cfg = cfg
        self.api = routeros_api.RouterOsApiPool(self.cfg['router_ip'],
                                                username=self.cfg['router_user'],
                                                password=self.cfg['router_password'],
                                                plaintext_login=True).get_api()

    def provision(self):
        print("==%20s ==" % datetime.now().strftime("%B %d %H:%m"))
        networks = self.get_networks()
        print(" * Total networks:", len(networks))
        print("=" * 25)
        if self.is_network_changed(networks):
            total_deleted = self.delete_old_networks(networks)
            print(" - Total deleted:", total_deleted)
            total_added = self.add_new_networks(networks)
            print(" + Total added:", total_added)
        else:

            print("== Network not changed ==")
        print("=" * 25)

    def get_existing_networks(self):
        routes = self.api.get_resource("/ip/route").get(comment=self.cfg['comment_for_routing'])
        return [x['dst-address'] for x in routes]

    def get_ips_by_hosts(self):
        ips = []
        for host in self.cfg['hosts']:
            if type(host) == str:
                ips.extend(socket.gethostbyname_ex(str(host))[2])
            elif type(host) == tuple:
                for i in range(host[1][0], host[1][1]):
                    ips.extend(socket.gethostbyname_ex(host[0] % i)[2])
        return ips

    def get_networks(self):
        ips = self.get_ips_by_hosts()
        networks = []
        for ip in ips:
            network = ip + "/32"
            if network not in networks:
                networks.append(network)
        networks.sort()
        return networks

    def is_network_changed(self, networks):
        networks_hash = "|".join(networks)
        if os.path.isfile(self.cfg['network_hash_file']):
            old_network_hash = open(self.cfg['network_hash_file']).read()
            if old_network_hash == networks_hash:
                return False
        open(self.cfg['network_hash_file'], "w").write(str(networks_hash))
        return True

    def delete_old_networks(self, new_networks):
        routes = self.api.get_resource("/ip/route").get(comment=self.cfg['comment_for_routing'])
        total_deleted = 0
        for route in routes:
            if route['dst-address'] not in new_networks:
                total_deleted += 1
                self.api.get_resource('/ip/route').remove(id=route['id'])
        return total_deleted

    def add_new_networks(self, networks):
        existing_networks = self.get_existing_networks()
        total_added = 0
        for network in networks:
            if network not in existing_networks:
                total_added += 1
                self.api.get_resource('/ip/route').add(dst_address=network,
                                                       gateway=self.cfg['gateway'],
                                                       comment=self.cfg['comment_for_routing'],
                                                       )
        return total_added


mikrotik = MikrotikVpnManager()
mikrotik.provision()
