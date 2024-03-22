import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import sys
import sqlmap
# import re # décommentez ceci pour DVWA

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"



def get_all_forms(url):
    """Cette fonction retourne tous les formulaires HTML du contenu de la page `url`"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    Cette fonction extrait toutes les informations utiles possibles sur un formulaire HTML `form`
    """
    details = {}
    # obtenir l'action du formulaire (URL cible)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    # obtenir la méthode du formulaire (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # obtenir tous les détails des entrées tels que le type et le nom
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # mettre toutes les informations dans le dictionnaire résultant
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


# def is_vulnerable(response):
#     """Une simple fonction booléenne qui détermine si une page est vulnérable à une injection SQL à partir de sa `response`"""
#     errors = {
#         # MySQL
#         "you have an error in your sql syntax;",
#         "warning: mysql",
#         # SQL Server
#         "unclosed quotation mark after the character string",
#         # Oracle
#         "quoted string not properly terminated",
#     }
#     for error in errors:
#         # si vous trouvez l'une de ces erreurs, retournez True
#         if error in response.content.decode().lower():
#             return True
#     # aucune erreur détectée
#     return False


def scan_sql_injection(url, wordlist):
    with open(wordlist, "r") as file:
        wordlist = file.read().splitlines()
    
    for c in wordlist:
        # ajouter le caractère de guillemet/apostrophe à l'URL
        new_url = f"{url}{c}"
        print("[!] Essai en cours", new_url)
        
        # utiliser sqlmap pour détecter les vulnérabilités d'injection SQL
        result = sqlmap.scan(url=new_url)
        
        if result.success:
            print("[+] Vulnérabilité d'injection SQL détectée, lien :", new_url)
            return
    
    print("Aucune vulnérabilité d'injection SQL détectée.")

if __name__ == "__main__":
    url = sys.argv[1]
    scan_sql_injection(url, "../wordlist/SecLists/Fuzzing/SQLi/Generic-SQLi.txt")

print
if __name__ == "__main__":
    url = sys.argv[1]
    scan_sql_injection(url, "../wordlist/SecLists/Fuzzing/SQLi/Generic-SQLi.txt")
