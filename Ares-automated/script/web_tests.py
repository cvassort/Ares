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
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    csv_file_path = os.path.join(dirb_folder_path, f'{target}_dirb.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for file in os.listdir(dirb_folder_path):
            dirb_file_path = os.path.join(dirb_folder_path, file)
            with open(dirb_file_path, 'r') as dirb_file:
                for line in dirb_file:
                    if line.startswith('+'):
                        directory = line.split()[1]
                        if directory.startswith(','):
                            directory = directory[1:]
                        writer.writerow([directory])


def get_directory_dirb(target,folder_path):
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    os.makedirs(dirb_folder_path, exist_ok=True)
    # Open dirb file and get directory for the target
    dirb_file_path = os.path.join(dirb_folder_path, f"{target}_dirb.csv")
    with open(dirb_file_path, "r") as dirb_file:
        valid_url = dirb_file.readlines()
    return valid_url

# def find_forms(valid_url):
#     url = valid_url
#     print(f"Finding login forms on {url}")
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     response = requests.get(url, headers=headers, verify=False)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     login_forms = []
#     forms = soup.find_all('form')
#     for form in forms:
#         inputs = form.find_all('input')
#         input_types = [input.get('type', '') for input in inputs]
#         if 'password' in input_types and 'text' in input_types and 'submit' in input_types:
#             forms.append(form)
#     return forms



# def get_form_details(form):
#     details = {}
#     action = form.attrs.get("action", "").lower()
#     method = form.attrs.get("method", "get").lower()
#     inputs = []
#     for input_tag in form.find_all("input"):
#         input_type = input_tag.attrs.get("type", "text")
#         input_name = input_tag.attrs.get("name")
#         inputs.append({"type": input_type, "name": input_name})
#     details["action"] = action
#     details["method"] = method
#     details["inputs"] = inputs
#     return details

# def submit_form(form_details, url, payload):
#     target_url = urljoin(url, form_details["action"])
#     data = {}
#     for input in form_details["inputs"]:
#         if input["type"] == "text" or input["type"] == "search":
#             data[input["name"]] = payload
#     print(f"Submitting form with payload: {payload}")
#     if form_details["method"] == "post":
#         response = requests.post(target_url, data=data, verify=False)
#     else:
#         response = requests.get(target_url, params=data, verify=False)
#     print(f"Response: {response.text}")
#     return response

def test_xss_with_xsstrike(valid_url, folder_path, target):
    print(f"Testing XSS on {valid_url} using XSStrike")
    xss_dir_path = os.path.join(folder_path, "xss")
    os.makedirs(xss_dir_path, exist_ok=True)
    xss_file_path = os.path.join(xss_dir_path, f"{target}.txt")
    
    try:
        # Construire la commande XSStrike
        xsstrike_command = [
            'python3 /XSStrike/xsstrike.py', '-u', valid_url, '--crawl', '--output', xss_file_path
        ]
        
        # Exécuter la commande XSStrike
        result = subprocess.run(xsstrike_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Lire la sortie de XSStrike
        output = result.stdout.decode('utf-8')
        errors = result.stderr.decode('utf-8')
        
        # Vérifier les vulnérabilités
        if 'VULNERABLE' in output:
            print("XSS vulnerability found!")
            with open(xss_file_path, "a") as xss_file:
                xss_file.write(valid_url + '\n')
                xss_file.write(output)
        else:
            print("No XSS vulnerability found.")
        
        # Afficher les erreurs s'il y en a
        if errors:
            print(f"Errors: {errors}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def test_sqli_with_sqlmap(valid_url, folder_path, target):
    print(f"Testing SQLi on {valid_url} using sqlmap")
    sqli_dir_path = os.path.join(folder_path, "sqli")
    os.makedirs(sqli_dir_path, exist_ok=True)
    sqli_file_path = os.path.join(sqli_dir_path, f"{target}_sqlmap.json")
    
    try:
        # Construire la commande sqlmap
        sqlmap_command = [
            'sqlmap', '-u', valid_url,'a', '--batch', '--forms','--csv-del=CSVDEL', '--output-dir', sqli_dir_path
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
    convert_dirb_output_to_csv(target, folder_path)
    valids_url = get_directory_dirb(target, folder_path)
    print(f"Running security tests on {target}")
    for valid_url in valids_url:
            test_xss_with_xsstrike(valid_url, folder_path, target)
            test_sqli_with_sqlmap(valid_url, folder_path, target)

