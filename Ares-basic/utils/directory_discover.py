import requests

def brute_force_directories(url, wordlist='../wordlist/SecLists/Discovery/Web-Content/big.txt'):
  with open(wordlist, 'r') as file:
    for line in file:
      directory = line.strip()
      full_url = url + '/' + directory
      
      response = requests.get(full_url)
      if response.status_code == 200:
        print(f"\033[92mDirectory found: {full_url} code : {response.status_code} ok\033[0m")
      elif response.status_code == 403:
        print(f"\033[93mDirectory found: {full_url} code : {response.status_code} forbidden\033[0m")
      elif response.status_code == 401:
        print(f"\033[93mDirectory found: {full_url} code : {response.status_code} unauthorized\033[0m")



brute_force_directories( 'https://www.hack-me.fr/', '../wordlist/SecLists/Discovery/Web-Content/big.txt')

