import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Metals API raktas (tiesiogiai įrašytas į kodą)
METALS_API_KEY = "gi5giv16mmkcrq8t195nxcoq4fm80otc2grz9j6kh8kpanzq58hl493d96p7"

# Metals API URL
METALS_API_URL = f"https://metals-api.com/api/latest?access_key={METALS_API_KEY}&base=USD&symbols=XAU,XAG,XPT,XPD"

@app.route('/')
def home():
    return "Hello, Railway!"

@app.route('/sxbx_price', methods=['GET'])
def get_sxbx_price():
    try:
        response = requests.get(METALS_API_URL)
        data = response.json()

        # Pridėtas testavimas: patikrinti, ar API grąžina teisingas kainas
        print("Metals API atsakymas:", data)

        # Patikrinam, ar nėra klaidų gautuose duomenyse
        if "rates" not in data or not all(k in data["rates"] for k in ["XAU", "XAG", "XPT", "XPD"]):
            return jsonify({"error": "Neteisingi API duomenys"}), 500

        # Metalų kainos API grąžina kaip "1 USD vertė metaluose", todėl reikia invertuoti
        gold_price_per_oz = 1 / data["rates"]["XAU"]
        silver_price_per_oz = 1 / data["rates"]["XAG"]
        platinum_price_per_oz = 1 / data["rates"]["XPT"]
        palladium_price_per_oz = 1 / data["rates"]["XPD"]

        # Patikrinam, ar skaičiavimai normalūs
        print(f"Auksas: {gold_price_per_oz}, Sidabras: {silver_price_per_oz}, Platina: {platinum_price_per_oz}, Paladis: {palladium_price_per_oz}")

        # Konvertuojame į kainą už gramą
        gold_price = gold_price_per_oz / 31.1035
        silver_price = silver_price_per_oz / 31.1035
        platinum_price = platinum_price_per_oz / 31.1035
        palladium_price = palladium_price_per_oz / 31.1035

        # SXBX mišinio formulė
        mix_price_per_gram = (
            (gold_price * 0.60) +
            (silver_price * 0.25) +
            (platinum_price * 0.10) +
            (palladium_price * 0.05)
        )

        # 1 SXBX = 0.025 g metalo mišinio
        sxbx_price = mix_price_per_gram * 0.025

        print(f"SXBX kaina: {sxbx_price}")  # Patikrinam, ar kaina reali

        return jsonify({"sxbx_price": round(sxbx_price, 4)})

    except Exception as e:
        print("Klaida:", str(e))  # Parodyti klaidą terminale
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



