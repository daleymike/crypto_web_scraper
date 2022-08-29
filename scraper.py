from bs4 import BeautifulSoup
import pandas as pd 
import requests
import json

def fetch_data():
    r = requests.get("https://www.coingecko.com/")

    if r.status_code == 200:
        print("SUCCESS")
        return r.text
    else:
        raise Exception("Error Occured")

def extract_crypto_info(html):
    soup = BeautifulSoup(html, "html.parser")

    coin_table = soup.find("div", {"class": "coin-table"})
    crypto_elements = coin_table.find_all("tr")[1:]

    cryptos = []

    for crypto in crypto_elements:
        cryptos.append({
            "name": crypto.find("td", {"class": "coin-name"})["data-sort"],
            "price": crypto.find("td", {"class": "td-price"}).text.strip(),
            "change_1hr": crypto.find("td", {"class": "td-change1h"}).text.strip(),
            "change_24hr": crypto.find("td", {"class": "td-change24h"}).text.strip(),
            "change_7d": crypto.find("td", {"class": "td-change7d"}).text.strip()
        })

    return cryptos

html = fetch_data()
cryptos = extract_crypto_info(html)


for crypto in cryptos:
    print(crypto, "\n")

with open("crypto.json", "w") as f:
    f.write(json.dumps(cryptos, indent=2))

crypt_json = pd.read_json('crypto.json')
crypt_json.to_excel('crypto.xlsx')


