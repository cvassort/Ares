import subprocess
import re
import os

def run_nmap_scan(target, folder_path):
    nmap_folder_path = os.path.join(folder_path, 'nmap')
    os.makedirs(nmap_folder_path, exist_ok=True)
    ip = ''
    port = ''
    print(f"Running nmap scan on {target}")
    if ':' in target:
        
        ip, port = target.split(':')
        print(f"Running nmap scan ond dozapo japoj {ip}")
        nmap_output = subprocess.run(['nmap', '-A', '-sV', '-p', port, ip, '-o', os.path.join(nmap_folder_path, f'{ip}:{port}_nmap.txt'), '-T4'], capture_output=True, text=True)

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
        nmap_output = subprocess.run(['nmap','sC', '-sV','-p-', '--open', '-o',os.path.join(nmap_folder_path, f'{ip}_nmap.txt'), ip , '-T4'], capture_output=True, text=True)

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
        subprocess.run(['nuclei', '-target', target,'-t','/nuclei-templates/', '-o', os.path.join(nuclei_folder_path, f'{ip}:{port}_nuclei.txt')])

def run_whatweb_scan(target, ip_ports, folder_path):
    whatweb_folder_path = os.path.join(folder_path, 'whatweb')
    os.makedirs(whatweb_folder_path, exist_ok=True)
    print(f"Running whatweb scan on {target}")
    for ip, port in ip_ports:
        target_url = f"http://{ip}:{port}"
        output_file = os.path.join(whatweb_folder_path, f'{ip}:{port}_whatweb.txt')
        try:
            subprocess.run(['whatweb', target_url, '-v', '--log-verbose', output_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during WhatWeb scan on {target_url}: {e}")

def run_wapiti_scan(target, ip_ports, folder_path):
    wapiti_folder_path = os.path.join(folder_path, 'wapiti')
    os.makedirs(wapiti_folder_path, exist_ok=True)
    print(f"Running wapiti scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        subprocess.run(['wapiti', '-u', f"http://{target}/",'-m', 'xss,sql,lfi,xxe,csrf,brute_login_form,blindsql,backup,buster,cookieflags,crlf,csp,exec,file,htaccess,http_headers,methods,nikto,permanentxss,redirect,shellshock,ssrf','-l', '2','-S','normal','-f','txt', '-o', os.path.join(wapiti_folder_path, f'{ip}:{port}_wapiti.txt')])

def run_nikto_scan(target, ip_ports, folder_path):
    nikto_folder_path = os.path.join(folder_path, 'nikto')
    os.makedirs(nikto_folder_path, exist_ok=True)
    print(f"Running nikto scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        subprocess.run(['nikto', '-h', target, '-C','-Format+','txt', '-o', os.path.join(nikto_folder_path, f'{ip}:{port}_nikto.txt')])

def run_dirb_scan(target, ip_ports, folder_path):
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    os.makedirs(dirb_folder_path, exist_ok=True)
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        print(f"Running dirb scan on {target}")
        subprocess.run(['dirb', f"http://{target}/", 'wordlists/big.txt', '-o', os.path.join(dirb_folder_path, f'{ip}:{port}_dirb.txt')])




def scan_target(target, folder_path):
    ip_ports = run_nmap_scan(target,folder_path)
    print(ip_ports)
    run_nuclei_scan(target, ip_ports,folder_path)
    run_whatweb_scan(target, ip_ports,folder_path)
    run_wapiti_scan(target, ip_ports,folder_path)
    run_nikto_scan(target, ip_ports,folder_path)
    run_dirb_scan(target, ip_ports,folder_path) 