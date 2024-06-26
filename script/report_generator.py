import os
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML
import matplotlib.pyplot as plt
from script.parse import load_file_content, extract_essential_nmap_info, extract_essential_nuclei_info, get_open_ports, filter_dirb_content

def generate_nuclei_graph(nuclei_results, output_path):
    """
    Génère un graphique des résultats de Nuclei.

    Args:
        nuclei_results (list): Une liste de résultats de Nuclei.
        output_path (str): Le chemin de sortie pour enregistrer le graphique.

    Returns:
        None

    Raises:
        None
    """
    levels = ['info', 'low', 'medium', 'high', 'critical']
    level_counts = {level: 0 for level in levels}

    for result in nuclei_results:
        for line in result.split('<br>'):
            for level in levels:
                if level in line.lower():
                    level_counts[level] += 1

    # Génération du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(level_counts.keys(), level_counts.values(), color=['blue', 'green', 'yellow', 'orange', 'red'])
    plt.xlabel('Severity Level')
    plt.ylabel('Count')
    plt.title('Nuclei Scan Results Severity Distribution')
    plt.savefig(output_path)
    plt.close()
    print(f"Graph generated and saved to {output_path}")


def generate_html_report(target, folder_path):
    """
    Génère un rapport HTML à partir des résultats des scans.
    """
    ip, port = target.split(':') if ':' in target else (target, None)
    print(f"Generating report for {ip}:{port}")

    # Chemin vers le fichier Nmap
    nmap_file = os.path.join(folder_path, 'nmap', f'{ip}_nmap.txt')
    if os.path.exists(nmap_file):
        with open(nmap_file, 'r') as file:
            nmap_content = file.read()
            ip_line = [line for line in nmap_content.split('\n') if 'Nmap scan report for' in line]
            if ip_line:
                ip_line = ip_line[0]
                ip = ip_line.split()[-1]
            else:
                print(f"Could not find 'Nmap scan report for' line in {nmap_file}")
                return "Error: 'Nmap scan report for' line not found"

            # Extraction des informations essentielles de Nmap
            essential_nmap_info = extract_essential_nmap_info(nmap_content)

            # Chemins des fichiers de scan pour chaque type de scan
            scan_files = {
                'Nmap': [os.path.join(folder_path, 'nmap', f'{ip}_nmap.txt')],
                'Nuclei': [os.path.join(folder_path, 'nuclei', f'{ip}:{port}_nuclei.txt') for port in get_open_ports(nmap_content)],
                'Wapiti': [os.path.join(folder_path, 'wapiti', f'{ip}:{port}_wapiti.txt') for port in get_open_ports(nmap_content)],
                'WhatWeb': [os.path.join(folder_path, 'whatweb', f'{ip}:{port}_whatweb.txt') for port in get_open_ports(nmap_content)],
                'Nikto': [os.path.join(folder_path, 'nikto', f'{ip}:{port}_nikto.txt' if port else f'{ip}_nikto.txt') for port in get_open_ports(nmap_content)],
                'Dirb': [os.path.join(folder_path, 'dirb', f'{ip}:{port}_dirb.txt')] if port else [],
                'XSS': [os.path.join(folder_path, 'xss', f'{ip}:{port}_xss.txt') for port in get_open_ports(nmap_content)],
                'SQLi': [os.path.join(folder_path, 'sqli', f'{ip}:{port}_sqli.txt') for port in get_open_ports(nmap_content)]
            }

            # Résultats des scans
            scan_results = {}
            for name, paths in scan_files.items():
                scan_results[name] = []
                for path in paths:
                    if os.path.exists(path) and os.path.isfile(path):
                        content = load_file_content(path)
                        if name == 'Nuclei':
                            content = extract_essential_nuclei_info(content)
                        elif name == 'Dirb':
                            content = filter_dirb_content(content, ip, port)
                        if content.strip():
                            scan_results[name].append(content)
                    else:
                        print(f"File not found: {path} for {name} on port {port}")
                        scan_results[name].append(f"File not found: {path} for {name} on port {port}")

            # Générer et inclure le graphique des résultats Nuclei
            nuclei_graph_path = os.path.join(folder_path, 'nuclei_graph.png')
            generate_nuclei_graph(scan_results['Nuclei'], nuclei_graph_path)

            # Conversion des listes en chaînes HTML
            for name in scan_results:
                scan_results[name] = '<br>'.join(scan_results[name])

            # Lecture du template HTML et rendu avec les résultats des scans
            with open('./script/report_template.html', 'r') as file:
                template = Template(file.read())

            # Date actuelle pour le rapport
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_content = template.render(target=target, date=date_str, scan_results=scan_results, nuclei_graph_path=nuclei_graph_path, essential_nmap_info=essential_nmap_info)

            return html_content
    else:
        print(f"File not found: {nmap_file}")
        return "Error: File not found"

    return "Error: Unexpected error occurred"






def generate_pdf_report(target, folder_path):
    """
    Génère un rapport PDF à partir des résultats des scans.
    
    """
    html_content = generate_html_report(target, folder_path)
    output_html_path = os.path.join(folder_path, f'{target}_scan_report.html')
    output_pdf_path = os.path.join(folder_path, f'{target}_scan_report.pdf')

    # Sauvegarde du rapport HTML
    with open(output_html_path, 'w') as file:
        file.write(html_content)

    # Génération du PDF à partir du HTML
    HTML(output_html_path).write_pdf(output_pdf_path)
    print(f"HTML report saved to {output_html_path}")
    print(f"PDF report saved to {output_pdf_path}")
