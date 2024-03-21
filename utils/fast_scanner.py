import nmap

def scan_nmap(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-O -sV -p-')
    print(f"Host: {target} \n nm hosts: {nm.all_hosts()}")
    for host in nm.all_hosts():
        os_result = nm[host]['osmatch']
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        port_result = []
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                port_info = {
                    "port": port,
                    "state": nm[host][proto][port]['state'],
                    "name": nm[host][proto][port]['name'],
                    "product": nm[host][proto][port]['product'],
                    "version": nm[host][proto][port]['version']
                }
                print(port_info)
                port_result.append(port_info)

    
    return port_result, os_result