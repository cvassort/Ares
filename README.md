# Projet Ares

Le projet **Ares** est une application de sécurité destinée à l'analyse et à la génération de rapports à partir de scans de sécurité sur des cibles spécifiques.








## TODO
 - [ ] integration de wpscan pour scan les sites wordpress
 - [ ] Wafwoof
 - [ ] faire un output en csv ou json
 - [ ] mettre des options pour faire un scan plus rapide
 - [x] mise en place dans un docker
 - [x] export en pdf et html
 - [ ] Amelioration des fonctions de test xss et sql injection
 - [ ] Amelioration de nikto


## Fonctionnalités

- **Analyse de Sécurité** : Effectue des scans détaillés pour identifier les vulnérabilités potentielles.
- **Génération de Rapports** : Crée un rapport pour chaque ip. Le rapport est sous format pdf et html
- **Support Multi-scans** : Prend en charge plusieurs types de scans tels que Nmap, Nuclei, Wapiti, WhatWeb, Nikto, Dirb, XSS et SQLi.

## Installation

1. **Prérequis** :
   docker d'installer : https://www.docker.com/products/docker-desktop/

2. **Clonage du Projet** :
   ```bash
   git clone https://github.com/cvassort/Ares.git
   cd Ares
   ```
3. **Configuration**
    les configurations ce font dans le `target.txt`. Il faudra mettre les IPs dans ce fichier avant le build du docker. 

4. **Déploiement(docker)**
   Lors de la commande docker tout les fichiers, dépendances seront installer.
    ```bash
    docker-compose up -d --build
    ````
5. **Récuperation des rapports**
   Le rapport généré sera enregistré dans le dossier `./results` avec les détails spécifiques de votre cible.
   

## Structure du projet
    ```plaintext
    .
    ├── README.md                      # Fichier de documentation du projet
    ├── docker-compose.yml             # Configuration de Docker Compose pour l'application
    ├── dockerfile                     # Dockerfile pour créer l'image Docker de l'application
    ├── main.py                        # Script principal pour lancer l'application
    ├── requirements.txt               # Fichier listant les dépendances Python du projet
    ├── script                         # Répertoire contenant les scripts du projet
    │   ├── parse.py                   # Script pour analyser les résultats des scans
    │   ├── report_generator.py        # Script pour générer les rapports de scan
    │   ├── report_template.html       # Template HTML pour les rapports
    │   ├── scanner.py                 # Script pour exécuter les scans de sécurité
    │   ├── styles.css                 # Styles CSS pour le rapport HTML
    │   └── web_tests.py               # Script pour effectuer des tests de sécurité sur le web
    ├── targets.txt                    # Fichier listant les cibles à scanner
    └── wordlists                      # Répertoire contenant les listes de mots pour les attaques
        ├── big.txt                    # Grande liste de mots pour les attaques de force brute
        ├── sqli_payloads.txt          # Payloads pour les attaques SQL injection
        └── xss_payloads.txt           # Payloads pour les attaques XSS
    ```



## `main.py`

### Description et But du Fichier

Le fichier `main.py` est le point d'entrée principal de l'application de test de sécurité automatisé. Il utilise les arguments en ligne de commande pour scanner une ou plusieurs cibles spécifiées et générer des rapports détaillés basés sur les résultats des scans.

### Fonctionnalités Principales

- **Argument Parser (`argparse`)** : Gère les options en ligne de commande pour spécifier soit une cible unique (`-t` / `--target`) soit un fichier contenant plusieurs cibles (`-f` / `--file`).
- **Lecture des Cibles** : Fonction `read_targets_from_file` pour extraire les cibles à partir d'un fichier spécifié.
- **Scanning et Tests de Sécurité** : Utilisation de `scan_target` depuis `scanner.py` pour effectuer les scans de sécurité et de `run_security_tests` depuis `web_tests.py` pour les tests de sécurité supplémentaires (commenté dans le code).
- **Génération de Rapports PDF** : Appelle `generate_pdf_report` depuis `report_generator.py` pour créer des rapports PDF structurés à partir des résultats des scans.

### Gestion des Ressources

- **Création de Dossiers** : Crée un dossier spécifique pour chaque cible scannée dans le répertoire `results`, en utilisant une structure de nommage basée sur la cible et la date.
- **Copie de Fichier CSS** : Copie le fichier CSS de style (`styles.css`) dans le dossier de résultats pour personnaliser l'apparence des rapports générés.



## `scanner.py`

### Description et But du Fichier

Le fichier `scanner.py` contient des fonctions pour effectuer différents types de scans de sécurité sur une cible spécifiée. Ces scans incluent l'utilisation d'outils comme Nmap, Nuclei, WhatWeb, Wapiti, Nikto, et Dirb pour identifier les vulnérabilités et les failles potentielles sur les systèmes cibles.

### Fonctions et Objectifs

- **run_nmap_scan** : Cette fonction utilise l'outil Nmap pour scanner les ports ouverts d'une cible spécifiée. Elle extrait également les ports ouverts à partir du résultat du scan pour une analyse plus approfondie.

- **run_nuclei_scan** : Fonction pour lancer un scan avec Nuclei sur les cibles identifiées par `run_nmap_scan`. Nuclei est un outil de scanner de vulnérabilité flexible qui permet de tester plusieurs types d'attaques sur les applications web.

- **run_whatweb_scan** : Cette fonction utilise WhatWeb pour scanner les technologies web utilisées par la cible, fournissant des informations détaillées sur les technologies détectées.

- **run_wapiti_scan** : Fonction pour exécuter un scan avec Wapiti, un outil de sécurité pour les applications web, identifiant les vulnérabilités de sécurité comme les injections SQL, les traversées de répertoire, etc.

- **run_nikto_scan** : Cette fonction utilise Nikto pour effectuer un scan de sécurité complet sur les serveurs web, identifiant les vulnérabilités et les configurations incorrectes.

- **run_dirb_scan** : Fonction pour lancer un scan de brute force de répertoire avec Dirb, un outil pour découvrir des répertoires et des fichiers cachés sur des serveurs web.

- **scan_target** : Fonction principale qui orchestre le processus de scan en appelant `run_nmap_scan` et potentiellement d'autres fonctions de scan pour générer des rapports détaillés sur les vulnérabilités trouvées.

### Utilisation et Gestion des Ressources

- Chaque fonction crée des dossiers spécifiques dans le répertoire de résultats (`results`) pour sauvegarder les résultats de chaque scan effectué.

- Les résultats sont enregistrés dans des fichiers texte pour permettre une analyse ultérieure et la génération de rapports détaillés.

### Commentaires

Ce fichier est essentiel pour l'automatisation des scans de sécurité et la détection des vulnérabilités sur les cibles spécifiées, contribuant ainsi à renforcer la sécurité des systèmes informatiques contre les cyberattaques.


## `web_tests.py`

### Description et But du Fichier

Le fichier `web_tests.py` contient des fonctions pour effectuer des tests de sécurité automatisés sur des applications web. Ces tests visent principalement à détecter des vulnérabilités courantes comme les attaques XSS (Cross-Site Scripting) et les injections SQL (SQL Injection) sur les URL validées à l'aide de l'outil Dirb.

### Fonctions et Objectifs

- **convert_dirb_output_to_csv** : Cette fonction convertit la sortie du scan Dirb en format CSV pour faciliter l'analyse des répertoires découverts. Elle extrait les répertoires validés à partir des fichiers textes générés par Dirb et les écrit dans un fichier CSV.

- **get_directory_dirb** : Fonction pour récupérer les répertoires validés à partir du fichier CSV généré par Dirb pour une cible spécifique. Ces répertoires seront utilisés comme entrées pour les tests de sécurité XSS et SQLi.

- **test_xss_with_xsstrike** : Cette fonction utilise l'outil XSStrike pour tester les vulnérabilités XSS sur les URL validées. Elle crée un fichier de sortie contenant les résultats du scan XSStrike et vérifie la présence de vulnérabilités XSS dans les réponses des applications web.

- **test_sqli_with_sqlmap** : Fonction pour tester les vulnérabilités SQL Injection (SQLi) sur les URL validées à l'aide de l'outil sqlmap. Elle crée un fichier de sortie contenant les résultats du scan sqlmap et vérifie la présence de vulnérabilités SQLi dans les réponses des applications web.

- **run_security_tests** : Fonction principale qui orchestre le processus de tests de sécurité pour une cible spécifique. Elle appelle `convert_dirb_output_to_csv` pour préparer les données, récupère les répertoires validés avec `get_directory_dirb`, puis exécute les tests XSS et SQLi sur chaque URL validée.

### Utilisation et Gestion des Ressources

- Chaque fonction crée des dossiers spécifiques dans le répertoire de résultats (`results`) pour sauvegarder les résultats des tests de sécurité.

- Les résultats des tests XSS et SQLi sont enregistrés dans des fichiers texte pour permettre une analyse détaillée des vulnérabilités détectées.

### Commentaires

Ce fichier est crucial pour l'automatisation des tests de sécurité des applications web, en identifiant et en signalant les vulnérabilités XSS et SQLi potentielles. Il contribue à renforcer la sécurité des systèmes en détectant et en corrigeant ces vulnérabilités avant qu'elles ne soient exploitées par des attaquants.




## `parse.py`

### Description et But du Fichier

Le fichier `parse.py` contient diverses fonctions d'analyse et de traitement du contenu des fichiers de sortie générés par les outils de scan de sécurité comme Nmap, Nuclei et Dirb. Le but principal de ce fichier est d'extraire et de formater les informations essentielles des rapports de ces outils pour les intégrer dans des rapports HTML.

### Fonctions et Objectifs

- **load_file_content** :
  - **Description** : Charge le contenu d'un fichier et remplace les sauts de ligne par des balises `<br>` pour un rendu HTML.
  - **Objectif** : Faciliter l'intégration du contenu brut des fichiers de sortie dans un format HTML pour les rapports.

- **extract_essential_nmap_info** :
  - **Description** : Extrait les informations essentielles des résultats de scan Nmap et les formate sous forme de tableau HTML.
  - **Objectif** : Présenter les résultats clés des scans Nmap (ports ouverts et services associés) de manière lisible et structurée dans les rapports HTML.

- **extract_essential_nuclei_info** :
  - **Description** : Extrait et retourne les informations essentielles des résultats de Nuclei.
  - **Objectif** : Filtrer et formater les informations pertinentes des scans Nuclei pour les inclure dans les rapports HTML.

- **get_open_ports** :
  - **Description** : Récupère et retourne une liste des ports ouverts à partir du contenu des résultats de scan Nmap.
  - **Objectif** : Identifier rapidement les ports ouverts à des fins d'analyse ultérieure et de tests de sécurité ciblés.

- **filter_dirb_content** :
  - **Description** : Filtre le contenu des résultats de Dirb pour ne conserver que les lignes pertinentes concernant les répertoires trouvés.
  - **Objectif** : Extraire et présenter les répertoires découverts par Dirb de manière concise pour faciliter l'analyse et les tests de sécurité supplémentaires.

### Utilisation et Gestion des Ressources

- Les fonctions utilisent des opérations de lecture de fichiers pour charger et traiter le contenu des rapports de scan.
- Le contenu filtré et formaté est ensuite utilisé pour générer des rapports HTML détaillés, intégrant les informations les plus pertinentes pour l'analyse de sécurité.

### Commentaires

Ce fichier joue un rôle crucial dans l'automatisation du processus de création de rapports de sécurité. En extrayant et en formatant les informations clés des différents outils de scan, il permet de générer des rapports clairs et utiles pour les analystes de sécurité. Il facilite également l'intégration des résultats dans des formats HTML, rendant les rapports plus accessibles et faciles à interpréter.




## report_generator.py

### Description et But du Fichier

Le fichier `report_generator.py` est conçu pour générer des rapports de sécurité détaillés sous forme de fichiers HTML et PDF à partir des résultats des différents outils de scan de sécurité (comme Nmap, Nuclei, Dirb, etc.). L'objectif principal de ce fichier est de collecter, organiser, et présenter les résultats des scans de manière claire et lisible pour les analystes de sécurité.

### Fonctions et Objectifs

- **generate_nuclei_graph** :
  - **Description** : Génère un graphique représentant la distribution des niveaux de sévérité des résultats de scan Nuclei.
  - **Objectif** : Visualiser rapidement les vulnérabilités détectées par Nuclei en fonction de leur niveau de gravité.

- **generate_html_report** :
  - **Description** : Génère un rapport HTML à partir des résultats des scans pour une cible donnée.
  - **Objectif** : Créer un rapport HTML détaillé et structuré incluant les résultats des différents outils de scan, ainsi que des graphiques pour une meilleure visualisation.

- **generate_pdf_report** :
  - **Description** : Génère un rapport PDF à partir des résultats des scans en utilisant le contenu du rapport HTML généré.
  - **Objectif** : Fournir un rapport de sécurité complet et portable en format PDF, qui peut être facilement partagé et archivé.

### Utilisation et Gestion des Ressources

- Les fonctions de ce fichier utilisent des fichiers de sortie générés par divers outils de scan pour extraire et formater les informations pertinentes.
- `generate_html_report` utilise le moteur de templates Jinja2 pour intégrer les résultats des scans dans un template HTML prédéfini.
- `generate_pdf_report` convertit ensuite ce rapport HTML en PDF à l'aide de WeasyPrint.
- Des graphiques sont générés avec Matplotlib pour visualiser les données des résultats Nuclei.

### Commentaires

Ce fichier est essentiel pour la création de rapports de sécurité automatisés, permettant aux analystes de gagner du temps et de se concentrer sur l'analyse des résultats plutôt que sur la compilation des rapports. Les rapports générés sont détaillés, lisibles et incluent des visualisations pour une meilleure interprétation des données de sécurité.








# Licence

Copyright (c) 2012-2024 Scott Chacon and others

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.