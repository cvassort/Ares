import requests

def brute_force_directories(url, wordlist):
  with open(wordlist, 'r') as file:
    for line in file:
      directory = line.strip()
      full_url = url + '/' + directory
      response = requests.get(full_url)
      if response.status_code == 200:
        print(f"Directory found: {full_url}")
        

