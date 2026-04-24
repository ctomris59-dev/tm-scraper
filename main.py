from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def get_tm_info(soup, label):
    element = soup.find("span", string=lambda t: t and label in t)
    return element.find_next("span").text.strip() if element else "—"

@app.route('/api/tm-fetch', methods=['GET'])
def fetch():
    url = request.args.get('url')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # Piyasa Değeri için özel arama
        val_div = soup.find("div", {"class": "tm-player-market-value-main-price"})
        val = val_div.text.strip().split(' ')[0] if val_div else "—"

        data = {
            "name": soup.find("h1").text.strip() if soup.find("h1") else "—",
            "age": get_tm_info(soup, "Yaş:"),
            "height": get_tm_info(soup, "Boy:"),
            "foot": get_tm_info(soup, "Ayak:"),
            "nationality": soup.find("span", {"itemprop": "nationality"}).text.strip() if soup.find("span", {"itemprop": "nationality"}) else "—",
            "position": get_tm_info(soup, "Mevki:"),
            "contract": get_tm_info(soup, "Sözleşme bitiş tarihi:"),
            "value": val
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
