import subprocess
import re
import os

def run_nmap_scan(target, folder_path):
    nmap_folder_path = os.path.join(folder_path, 'nmap')
    os.makedirs(nmap_folder_path, exist_ok=True)
    ip = ''
    port = ''

    if ':' in target:
        ip, port = target.split(':')
        print(f"Running nmap scan on {ip}")
        nmap_output = subprocess.run(['nmap', '-A', '-sV', '-p', port, '--open', '-O', ip, '-o', os.path.join(nmap_folder_path, f'{ip}_nmap.json'), '-T4'], capture_output=True, text=True)

        # Parse nmap output to extract open ports
        open_ports = []
        for line in nmap_output.stdout.split('\n'):
            # Match lines that contain open ports
            match = re.search(r'^(\d+)/tcp\s+open', line)
            if match:
                open_ports.append(match.group(1))

        # Return a list of tuples (ip, port)
        ip_ports = [(ip, port) for port in open_ports]
        
        return ip_ports
    else:
        ip = target
        print(f"Running nmap scan on {ip}")
        nmap_output = subprocess.run(['nmap', '-sV','-p-', '--open', '-oN',os.path.join(nmap_folder_path, f'{ip}_nmap.txt'), ip , '-T4'], capture_output=True, text=True)

        # Parse nmap output to extract open ports
        open_ports = []
        for line in nmap_output.stdout.split('\n'):
            # Match lines that contain open ports
            match = re.search(r'^(\d+)/tcp\s+open', line)
            if match:
                open_ports.append(match.group(1))

        # Return a list of tuples (ip, port)
        ip_ports = [(ip, port) for port in open_ports]
        
        return ip_ports


def run_nuclei_scan(target, ip_ports,folder_path):
    nuclei_folder_path = os.path.join(folder_path, 'nuclei')
    os.makedirs(nuclei_folder_path, exist_ok=True)
    
    print(f"Running nuclei scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        print(target)
        subprocess.run(['nuclei', '-target', target,'-t','/nuclei-templates/', '-o', os.path.join(nuclei_folder_path, f'{ip}_{port}_nuclei.csv')])

def run_whatweb_scan(target, ip_ports, folder_path):
    whatweb_folder_path = os.path.join(folder_path, 'whatweb')
    os.makedirs(whatweb_folder_path, exist_ok=True)
    print(f"Running whataweb scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        subprocess.run(['whatweb', target, os.path.join(whatweb_folder_path,f'--log-json-verbose={ip}_{port}_whatweb.json')])

def run_wapiti_scan(target, ip_ports, folder_path):
    wapiti_folder_path = os.path.join(folder_path, 'wapiti')
    os.makedirs(wapiti_folder_path, exist_ok=True)
    print(f"Running wapiti scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        subprocess.run(['wapiti', '-u', f"http://{target}/",'-m', 'xss,sql,lfi,xxe,csrf,brute_login_form,blindsql,backup,buster,cookieflags,crlf,csp,exec,file,htaccess,http_headers,methods,nikto,permanentxss,redirect,shellshock,ssrf,wapp','-l', '2','-S','normal','-f','xml', '-o', os.path.join(wapiti_folder_path, f'{ip}_{port}_wapiti.json')])

def run_nikto_scan(target, ip_ports, folder_path):
    nikto_folder_path = os.path.join(folder_path, 'nikto')
    os.makedirs(nikto_folder_path, exist_ok=True)
    print(f"Running nikto scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        subprocess.run(['nikto', '-h', target, '-C', '-Format', 'csv', '-o', os.path.join(nikto_folder_path, f'{ip}_{port}_nikto.csv')])

def run_dirb_scan(target, ip_ports, folder_path):
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    os.makedirs(dirb_folder_path, exist_ok=True)
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        print(f"Running dirb scan on {target}")
        subprocess.run(['dirb', f"http://{target}/", 'wordlists/big.txt','-X','.html,.php,.asp,.aspx,.jsp,.cgi,.pl,.py,.txt,.xml,.json,.js,.css,.jpg,.jpeg,.png,.gif,.bmp,.ico,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.mp3,.mp4,.avi,.mov,.zip,.tar,.gz,.rar' '-o', os.path.join(dirb_folder_path, f'{ip}_{port}_dirb.txt')])

def scan_target(target, folder_path):
    ip_ports = run_nmap_scan(target,folder_path)
    print(ip_ports)
    # run_nuclei_scan(target, ip_ports,folder_path)
    # run_whatweb_scan(target, ip_ports,folder_path)
    # run_wapiti_scan(target, ip_ports,folder_path)
    # run_nikto_scan(target, ip_ports,folder_path)
    run_dirb_scan(target, ip_ports,folder_path) 