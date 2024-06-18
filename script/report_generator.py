import os
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML, CSS
import textwrap

def load_file_content(file_path):
    print(f"Loading content from {file_path}")
    if os.path.isfile(file_path):  
        with open(file_path, 'r') as file:
            content = file.read()
            content_with_br = content.replace('\n', '<br>')
            return content_with_br
    return "File not found."

def extract_essential_nuclei_info(content):
    lines = content.split('<br>')
    essential_info = [line for line in lines if line.strip()]
    return '<br>'.join(essential_info)

def generate_html_report(target, folder_path):
    ip, port = target.split(':') if ':' in target else (target, None)

    print(f"Generating report for {ip}:{port}")
    nmap_file = os.path.join(folder_path, 'nmap', f'{ip}_nmap.txt')
    with open(nmap_file, 'r') as file:
        nmap_content = file.read()
        port_lines = [line for line in nmap_content.split('\n') if '/tcp' in line]
        ports = [line.split('/')[0] for line in port_lines]
        ip_line = [line for line in nmap_content.split('\n') if 'Nmap scan report for' in line][0]
        ip = ip_line.split()[-1]

    scan_files = {
        'Nmap': [os.path.join(folder_path, 'nmap', f'{ip}_nmap.txt')],
        'Nuclei': [os.path.join(folder_path, 'nuclei', f'{ip}:{port}_nuclei.txt') for port in ports],
        'Wapiti': [os.path.join(folder_path, 'wapiti', f'{ip}:{port}_wapiti.txt') for port in ports],
        'WhatWeb': [os.path.join(folder_path, 'whatweb', f'{ip}:{port}_whatweb.txt') for port in ports],
        'Nikto': [os.path.join(folder_path, 'nikto', f'{ip}:{port}_nikto.txt') for port in ports],
        'Dirb': [os.path.join(folder_path, 'dirb', f'{ip}:{port}_dirb.txt') for port in ports],
        'XSS': [os.path.join(folder_path, 'xss', f'{ip}:{port}_xss.txt') for port in ports],
        'SQLi': [os.path.join(folder_path, 'sqli', f'{ip}:{port}_sqli.txt') for port in ports]
    }

    scan_results = {}
    for name, paths in scan_files.items():
        scan_results[name] = []
        for path in paths:
            if os.path.exists(path) and os.path.isfile(path):
                content = load_file_content(path)
                if name == 'Nuclei':
                    content = extract_essential_nuclei_info(content)
                if content.strip():
                    scan_results[name].append(content)
            else:
                print(f"File not found: {path}")
                scan_results[name].append(f"File not found for {name} on port {path.split('_')[-1].split('.')[0]}")

    for name in scan_results:
        scan_results[name] = '<br>'.join(scan_results[name])

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

    pdf_styles = """
        @page { margin: 50px; }
        body { text-align: left; }
        .container { display: inline-block; text-align: left; width: 100%; max-width: 700px; }
        p { word-wrap: break-word; page-break-inside: avoid; }
    """
    
    wrapped_content = wrap_text(html_content, 50)  
    HTML(string=wrapped_content).write_pdf(pdf_file, stylesheets=[CSS(string=pdf_styles)])
    print(f"PDF report generated: {pdf_file}")

def wrap_text(content, max_length):
    lines = content.split('\n')
    wrapped_lines = []
    for line in lines:
        wrapped_line = textwrap.fill(line, width=max_length)
        wrapped_lines.append(wrapped_line)
    return '\n'.join(wrapped_lines)

def generate_report(target, folder_path):
    os.makedirs(folder_path, exist_ok=True)

    sub_dirs = ['nmap', 'nuclei', 'wapiti', 'whatweb', 'nikto', 'dirb', 'xss', 'sqli']
    for sub_dir in sub_dirs:
        os.makedirs(os.path.join(folder_path, sub_dir), exist_ok=True)

    generate_pdf_report(target, folder_path)

