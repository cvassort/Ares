import requests
import subprocess
from bs4 import BeautifulSoup
import urllib3
import os
from urllib.parse import urljoin
import csv

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def convert_dirb_output_to_csv(target, folder_path):
    """
    Converts the output of Dirb tool to a CSV file.

    Args:
        target (str): The target name.
        folder_path (str): The path to the folder containing the Dirb output files.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified folder_path does not exist.

    """
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    csv_file_path = os.path.join(dirb_folder_path, f'{target}_dirb.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for file in os.listdir(dirb_folder_path):
            if file.endswith('.txt'):
                dirb_file_path = os.path.join(dirb_folder_path, file)
                with open(dirb_file_path, 'r') as dirb_file:
                    for line in dirb_file:
                        if line.startswith('+'):
                            directory = line.split()[1]
                            if directory.startswith(','):
                                directory = directory[1:]
                            writer.writerow([directory])
    print(f"Dirb output converted to CSV. CSV file saved to {csv_file_path}")


def get_directory_dirb(target, folder_path):
    """
    Get the directory for the target using the DirBuster tool.

    Args:
        target (str): The target for which the directory is to be retrieved.
        folder_path (str): The path to the folder where the directory files will be stored.

    Returns:
        list: A list of valid URLs found in the directory file.

    """
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    os.makedirs(dirb_folder_path, exist_ok=True)
    # Open dirb file and get directory for the target
    dirb_file_path = os.path.join(dirb_folder_path, f"{target}_dirb.csv")
    with open(dirb_file_path, "r") as dirb_file:
        valid_urls = dirb_file.readlines()
    return valid_urls



def test_xss_with_xsstrike(valid_url, folder_path, target):
    """
    Test XSS vulnerabilities on a given URL using XSStrike.

    Args:
        valid_url (str): The valid URL to test for XSS vulnerabilities.
        folder_path (str): The folder path where the XSS results will be stored.
        target (str): The target IP address and port in the format 'ip:port'.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the XSS testing.

    """
    ip, port = target.split(':')
    print(f"Testing XSS on {valid_url.strip()} using XSStrike")
    xss_dir_path = os.path.join(folder_path, "xss")
    os.makedirs(xss_dir_path, exist_ok=True)
    xss_file_path = os.path.join(xss_dir_path, f"{ip}:{port}_xss.txt")
    
    try:
        # Construire la commande XSStrike
        xsstrike_command = [
            'python3', '/XSStrike/xsstrike.py', '-u', valid_url.strip(), '--crawl'
        ]
        
        # Exécuter la commande XSStrike
        with open(xss_file_path, 'w') as output_file:
            result = subprocess.run(xsstrike_command, stdout=output_file, stderr=subprocess.PIPE)
        
        # Lire les erreurs de XSStrike
        errors = result.stderr.decode('utf-8')
        
        # Vérifier les vulnérabilités
        with open(xss_file_path, 'r') as file:
            output = file.read()
        if 'VULNERABLE' in output:
            print("XSS vulnerability found!")
        else:
            print("No XSS vulnerability found.")
        
        # Afficher les erreurs s'il y en a
        if errors:
            print(f"Errors: {errors}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def test_sqli_with_sqlmap(valid_url, folder_path, target):
    """
    Test SQL injection vulnerability using sqlmap.

    Args:
        valid_url (str): The valid URL to test for SQL injection vulnerability.
        folder_path (str): The path to the folder where the SQL injection results will be stored.
        target (str): The target IP address and port in the format 'ip:port'.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the execution of the function.
    """
    ip, port = target.split(':')
    print(f"Testing SQLi on {valid_url.strip()} using sqlmap")
    sqli_dir_path = os.path.join(folder_path, "sqli")
    os.makedirs(sqli_dir_path, exist_ok=True)
    sqli_file_path = os.path.join(sqli_dir_path, f"{ip}:{port}_sqli.txt")
    
    try:
        # Construire la commande sqlmap
        sqlmap_command = [
            'sqlmap', '-u', valid_url.strip(), '--batch', '--forms', '--csv-del=CSVDEL', '--output-dir', sqli_dir_path
        ]
        
        # Exécuter la commande sqlmap
        result = subprocess.run(sqlmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Lire la sortie de sqlmap
        output = result.stdout.decode('utf-8')
        errors = result.stderr.decode('utf-8')
        
        # Vérifier les vulnérabilités
        if 'sqlmap identified the following injection point(s) with a total of' in output:
            print("SQLi vulnerability found!")
            with open(sqli_file_path, "a") as sqli_file:
                sqli_file.write(valid_url + '\n')
                sqli_file.write(output)
        else:
            print("No SQLi vulnerability found.")
        
        # Afficher les erreurs s'il y en a
        if errors:
            print(f"Errors: {errors}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def run_security_tests(target, folder_path):
    """
    Run security tests on the specified target.

    Args:
        target (str): The target URL or IP address.
        folder_path (str): The path to the folder where the test results will be stored.

    Returns:
        None
    """
    print(f"Converting dirb output to CSV for {target}")
    convert_dirb_output_to_csv(target, folder_path)
    valid_urls = get_directory_dirb(target, folder_path)
    print(f"Running security tests on {target}")
    for valid_url in valid_urls:
        test_xss_with_xsstrike(valid_url, folder_path, target)
        test_sqli_with_sqlmap(valid_url, folder_path, target)


