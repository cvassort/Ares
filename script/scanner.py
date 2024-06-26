import subprocess
import re
import os


def run_nmap_scan(target, folder_path):
    """
    Run an nmap scan on the specified target and save the results in the specified folder.

    Args:
        target (str): The target IP address or hostname.
        folder_path (str): The path to the folder where the nmap scan results will be saved.

    Returns:
        list: A list of tuples containing the IP address and open port numbers found during the scan.
    """
    nmap_folder_path = os.path.join(folder_path, 'nmap')
    os.makedirs(nmap_folder_path, exist_ok=True)
    ip = ''
    port = ''
    
    if ':' in target:
        ip, port = target.split(':')
        print(f"Running nmap scan on: {ip}")
        nmap_output = subprocess.run(['nmap', '-A', '-sV', '-p', port, ip, '-Pn', '-oN', os.path.join(nmap_folder_path, f'{ip}_{port}_nmap.txt')], capture_output=True, text=True)
    else:
        ip = target
        print(f"Running nmap scan on: {ip}")
        nmap_output = subprocess.run(['nmap', ip,'-sC', '-sV', '-p-', '--open', '-Pn', '-oN', os.path.join(nmap_folder_path, f'{ip}_nmap.txt')], capture_output=True, text=True)

    print("Nmap output:", nmap_output.stdout)

    open_ports = []
    for line in nmap_output.stdout.split('\n'):

        match = re.search(r'^(\d+)\/(tcp|udp)\s+open', line)
        if match:
            open_ports.append(match.group(1))
    
    print("Open ports found:", open_ports)

    ip_ports = [(ip, port) for port in open_ports]
    
    return ip_ports



    
def run_nuclei_scan(target, ip_ports, folder_path):
    """
    Run nuclei scan on the specified target IP addresses and ports.

    Args:
        target (str): The target IP address.
        ip_ports (list): A list of tuples containing IP addresses and ports.
        folder_path (str): The folder path where the nuclei scan results will be saved.

    Returns:
        None
    """
    nuclei_folder_path = os.path.join(folder_path, 'nuclei')
    os.makedirs(nuclei_folder_path, exist_ok=True)
    
    print(f"Running nuclei scan on {target}")
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        print(target)
        subprocess.run(['nuclei', '-target', target, '-t', '/nuclei-templates/', '-o', os.path.join(nuclei_folder_path, f'{ip}:{port}_nuclei.txt')])



def run_whatweb_scan(target, ip_ports, folder_path):
    """
    Run a WhatWeb scan on the specified target.

    Args:
        target (str): The target to scan.
        ip_ports (list): A list of tuples containing IP addresses and ports to scan.
        folder_path (str): The folder path to store the scan results.

    Returns:
        None
    """
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
    """
    Run Wapiti scan on the specified target.

    Args:
        target (str): The target to scan.
        ip_ports (list): A list of tuples containing IP addresses and ports to scan.
        folder_path (str): The folder path to store the scan results.

    Returns:
        None
    """
    wapiti_folder_path = os.path.join(folder_path, 'wapiti')
    os.makedirs(wapiti_folder_path, exist_ok=True)
    print(f"Running wapiti scan on {target}")
    for ip, port in ip_ports:
        target_url = f"http://{ip}:{port}/"
        output_file = os.path.join(wapiti_folder_path, f'{ip}:{port}_wapiti.txt')
        try:
            subprocess.run(['wapiti', '-u', target_url, '-l', '2', '-S', 'normal', '-f', 'txt', '-o', output_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during Wapiti scan on {target_url}: {e}")



def run_nikto_scan(target, ip_ports, folder_path):
    """
    Run a Nikto scan on the specified target.

    Args:
        target (str): The target to scan.
        ip_ports (list): A list of tuples containing IP addresses and ports to scan.
        folder_path (str): The folder path where the scan results will be saved.

    Returns:
        None

    Raises:
        subprocess.TimeoutExpired: If the Nikto scan times out.
        subprocess.CalledProcessError: If an error occurs during the Nikto scan.
    """
    nikto_folder_path = os.path.join(folder_path, 'nikto')
    os.makedirs(nikto_folder_path, exist_ok=True)
    print(f"Running Nikto scan on {target}")
    for ip, port in ip_ports:
        target_url = f"http://{ip}:{port}"
        output_file = os.path.join(nikto_folder_path, f'{ip}:{port}_nikto.txt')
        print(f"Running Nikto scan on {target_url}")
        try:
            subprocess.run(['nikto', '-h', target_url, '-C', 'all', '-Format', 'txt', '-o', output_file], timeout=1800) 
        except subprocess.TimeoutExpired as e:
            print(f"Nikto scan on {target_url} timed out: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Error during Nikto scan on {target_url}: {e}")

def run_dirb_scan(target, ip_ports, folder_path):
    """
    Run a dirb scan on the specified target IP addresses and ports.

    Args:
        target (str): The target IP address.
        ip_ports (list): A list of tuples containing IP addresses and ports.
        folder_path (str): The folder path where the scan results will be saved.

    Returns:
        None
    """
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    os.makedirs(dirb_folder_path, exist_ok=True)
    for ip, port in ip_ports:
        target = f"{ip}:{port}"
        print(f"Running dirb scan on {target}")
        subprocess.run(['dirb', f"http://{target}/", 'wordlists/big.txt', '-o', os.path.join(dirb_folder_path, f'{ip}:{port}_dirb.txt')])




def scan_target(target, folder_path):
    """
    Perform a series of scans on the target.

    Args:
        target (str): The target to scan.
        folder_path (str): The folder path to save the scan results.

    Returns:
        None
    """
    ip_ports = run_nmap_scan(target, folder_path)
    run_nuclei_scan(target, ip_ports, folder_path)
    run_whatweb_scan(target, ip_ports, folder_path)
    run_wapiti_scan(target, ip_ports, folder_path)
    # run_nikto_scan(target, ip_ports, folder_path)
    run_dirb_scan(target, ip_ports, folder_path)
