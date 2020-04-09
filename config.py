import yaml


def extract_hosts(cfg_hosts):
    hosts = []
    for v in cfg_hosts:
        if type(v) == str:
            hosts.append(v)
        elif type(v) == dict:
            domain, subdomains = list(v.items())[0]

            if "%02d" in domain:
                for i in range(subdomains[0], subdomains[1]+1):
                    hosts.append(domain % i)
            else:
                hosts.append(domain)
                for subdomain in subdomains:
                    hosts.append(subdomain + "." + domain)
    return hosts


with open("config.yml", 'r') as yml_file:
    cfg = yaml.load(yml_file, Loader=yaml.FullLoader)
    cfg['hosts'] = extract_hosts(cfg['hosts'])
