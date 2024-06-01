import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from jinja2 import Template

def generate_report(target, folder_path):
    generate_pdf_report(target, folder_path)
    generate_html_report(target, folder_path)

def generate_pdf_report(target, folder_path):
    ip, port = target.split(':')
    
    nmap_folder_path = os.path.join(folder_path, 'nmap')
    nmap_file = os.path.join(nmap_folder_path, f'{target}_nmap.txt')
    if not os.path.exists(nmap_file):
        print(f"Error: The required file {nmap_file} does not exist.")
        return

    nuclei_folder_path = os.path.join(folder_path, 'nuclei')
    nuclei_file = os.path.join(nuclei_folder_path, f'{target}_nuclei.csv')
    if not os.path.exists(nuclei_file):
        print(f"Error: The required file {nuclei_file} does not exist.")
        return
    
    wapiti_folder_path = os.path.join(folder_path, 'wapiti')
    wapiti_file = os.path.join(wapiti_folder_path, f'{target}_wapiti.json')
    if not os.path.exists(wapiti_file):
        print(f"Error: The required file {wapiti_file} does not exist.")
        return
    
    whatweb_folder_path = os.path.join(folder_path, 'whatweb')
    whatweb_file = os.path.join(whatweb_folder_path, f'{target}_whatweb.json')
    if not os.path.exists(whatweb_file):
        print(f"Error: The required file {whatweb_file} does not exist.")
        return
    
    nikto_folder_path = os.path.join(folder_path, 'nikto')
    nikto_file = os.path.join(nikto_folder_path, f'{target}_nikto.txt')
    if not os.path.exists(nikto_file):
        print(f"Error: The required file {nikto_file} does not exist.")
        return
    
    dirb_folder_path = os.path.join(folder_path, 'dirb')
    dirb_file = os.path.join(dirb_folder_path, f'{target}_dirb.txt')
    if not os.path.exists(dirb_file):
        print(f"Error: The required file {dirb_file} does not exist.")
        return
    
    xss_folder_path = os.path.join(folder_path, 'xss')
    xss_file = os.path.join(folder_path, f'{target}_xss.txt')
    if not os.path.exists(xss_file):
        print(f"Error: The required file {xss_file} does not exist.")
        return
    
    sqli_folder_path = os.path.join(folder_path, 'sqli')
    sqli_file = os.path.join(folder_path, f'{target}_sqli.txt')
    if not os.path.exists(sqli_file):
        print(f"Error: The required file {sqli_file} does not exist.")
        return
    

    # pdf_file = f'{target}_report.pdf'
    # c = canvas.Canvas(pdf_file, pagesize=letter)
    # width, height = letter

    # c.drawString(100, height - 100, f"Security Report for {target}")

    # with open(nmap_file, 'r') as f:
    #     nmap_data = f.read()
    # with open(nuclei_file, 'r') as f:
    #     nuclei_data = f.read()

    # c.drawString(100, height - 150, "Nmap Scan Results:")
    # c.drawString(100, height - 170, nmap_data)

    # c.drawString(100, height - 200, "Nuclei Scan Results:")
    # c.drawString(100, height - 220, nuclei_data)

    # c.save()

def generate_html_report(target):
    ip, port = target.split(':')

    # if not os.path.exists(nmap_file):
    #     print(f"Error: The required file {nmap_file} does not exist.")
    #     return
    # with open(nmap_file, 'r') as f:f:
    #     nmap_data = f.read()
    # pdf_file = f'{target}_report.pdf'
    # c = canvas.Canvas(pdf_file, pagesize=letter)

    # width, height = letter

    # c.drawString(100, height - 100, f"Security Report for {target}")
    # c.drawString(100, height - 150, "Nmap Scan Results:")
    # c.drawString(100, height - 170, nmap_data)
    # c.save()
