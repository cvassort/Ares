FROM kalilinux/kali-rolling

# Mettre à jour les paquets et installer les dépendances
RUN apt update && apt upgrade -y && \
    apt install -y python3 python3-pip nmap dirb gobuster nuclei \
    whatweb nikto wapiti git wget curl sqlmap weasyprint libpango-1.0-0 \
    libpangoft2-1.0-0 libjpeg-dev libopenjp2-7-dev libffi-dev

WORKDIR /nuclei-templates
RUN git clone https://github.com/projectdiscovery/nuclei-templates.git

WORKDIR /
RUN git clone https://github.com/s0md3v/XSStrike.git
RUN pip3 install -r /XSStrike/requirements.txt

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py", "-f", "targets.txt"]
