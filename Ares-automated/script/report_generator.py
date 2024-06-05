import os
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML

def load_file_content(file_path):
    if os.path.isfile(file_path):  # Vérifiez que le chemin est bien un fichier
        with open(file_path, 'r') as file:
            return file.read()
    return "File not found."

def generate_html_report(target, folder_path):
    ip, port = target.split(':') if ':' in target else (target, None)
    scan_files = {
        'Nmap': os.path.join(folder_path, 'nmap', f'{ip}:{port}_nmap.txt'),
        'Nuclei': os.path.join(folder_path, 'nuclei', f'{ip}:{port}_nuclei.txt'),
        'Wapiti': os.path.join(folder_path, 'wapiti', f'{ip}:{port}_wapiti.txt'),
        'WhatWeb': os.path.join(folder_path, 'whatweb', f'{ip}:{port}_whatweb.txt'),
        'Nikto': os.path.join(folder_path, 'nikto', f'{ip}:{port}_nikto.txt'),
        'Dirb': os.path.join(folder_path, 'dirb', f'{ip}:{port}_dirb.txt'),
        'XSS': os.path.join(folder_path, 'xss', f'{ip}:{port}_xss.txt'),
        'SQLi': os.path.join(folder_path, 'sqli', f'{ip}:{port}_sqli.txt')
    }

    scan_results = {name: load_file_content(path) for name, path in scan_files.items()}

    with open('./script/report_template.html', 'r') as file:
        template = Template(file.read())

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = template.render(target=target, date=date_str, scan_results=scan_results)

    return html_content

def generate_pdf_report(target, folder_path):
    html_content = generate_html_report(target, folder_path)
    html_file = os.path.join(folder_path, f'{target}_report.html')
    pdf_file = os.path.join(folder_path, f'{target}_report.pdf')

    with open(html_file, 'w') as file:
        file.write(html_content)

    HTML(html_file).write_pdf(pdf_file)
    print(f"PDF report generated: {pdf_file}")

def generate_report(target, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    
    # Créez les sous-répertoires nécessaires
    sub_dirs = ['nmap', 'nuclei', 'wapiti', 'whatweb', 'nikto', 'dirb', 'xss', 'sqli']
    for sub_dir in sub_dirs:
        os.makedirs(os.path.join(folder_path, sub_dir), exist_ok=True)

    generate_pdf_report(target, folder_path)

















def generate_report(target, folder_path):
    generate_html_report(target, folder_path)
    generate_pdf_report(target, folder_path)