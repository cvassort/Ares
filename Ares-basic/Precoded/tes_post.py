import requests

url = "https://www.hack-me.fr/auth.php"
headers = {
  "Cookie": "PHPSESSID=988dk8cul4almnp83pahjalg9q",
  "Content-Type": "application/x-www-form-urlencoded",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
  "Referer": "https://www.hack-me.fr/index.php",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
}

data = {
  "login": "1234",
  "password": "helloworld",
  "submit": ""
}

response = requests.post(url, headers=headers, data=data)

print(response.text)
print(response)