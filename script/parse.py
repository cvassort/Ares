import os
import re

def load_file_content(file_path):
    """
    Charge le contenu d'un fichier et le retourne avec des balises <br> pour le format HTML.
    """
    print(f"Loading content from {file_path}")
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            content_with_br = content.replace('\n', '<br>')
            return content_with_br
    return "File not found."

def extract_essential_nmap_info(nmap_content):
    """
    Extrait les informations essentielles de Nmap sous forme de tableau HTML.
    """
    essential_info = []
    port_info = False
    
    for line in nmap_content.split('\n'):
        line = line.strip()
        
        if line.startswith("Nmap scan report for"):
            essential_info.append(f"<tr><td colspan='2'>{line}</td></tr>")
        
        elif line.startswith("PORT"):
            port_info = True
            essential_info.append("<tr><th>Port</th><th>Service</th></tr>")
        
        elif port_info:
            if line.startswith("|_") or line.startswith("Host script results:"):
                continue
            elif not line:
                port_info = False
            else:
                match = re.match(r'^(\d+)\/(\w+)\s+(\w+)\s+(.*)', line)
                if match:
                    port, protocol, state, service = match.groups()
                    essential_info.append(f"<tr><td>{port}/{protocol}</td><td>{service}</td></tr>")
    
    return '<table>' + ''.join(essential_info) + '</table>'

def extract_essential_nuclei_info(content):
    """
    Extrait les informations essentielles de Nuclei.
    """
    lines = content.split('<br>')
    essential_info = [line for line in lines if line.strip()]
    return '<br>'.join(essential_info)

def get_open_ports(nmap_content):
    """
    Récupère la liste des ports ouverts à partir du contenu du fichier Nmap.
    """
    open_ports = []
    for line in nmap_content.split('\n'):
        match = re.search(r'^(\d+)\/(tcp|udp)\s+open', line)
        if match:
            open_ports.append(match.group(1))
    return open_ports

def filter_dirb_content(content, ip, port):
    """
    Filtre le contenu de Dirb pour ne conserver que les lignes pertinentes.
    """
    lines = content.split('<br>')
    found_lines = [line for line in lines if '==> DIRECTORY:' in line]
    if not found_lines:
        found_lines.append(f'No directories found on port {port} for target {ip}.')
    return '<br>'.join(found_lines)
