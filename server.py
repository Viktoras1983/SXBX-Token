from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://metals-api.com/api/latest?access_key=gi5giv16mmkcrq8t195nxcoq4fm80otc2grz9j6kh8kpanzq58hl493d96p7&base=USD&symbols=XAU,XAG,XPT,XPD"

@app.route('/', methods=['POST'])
def get_metal_prices():
    try:
        response = requests.get(API_URL)

        if response.status_code != 200:
            return jsonify({"error": "Metal API error"}), 500

        data = response.json()
        
        metal_prices = {
            "gold": data["rates"]["USDXAU"],   # Auksas
            "silver": data["rates"]["USDXAG"], # Sidabras
            "platinum": data["rates"]["USDXPT"], # Platina
            "palladium": data["rates"]["USDXPD"] # Paladis
        }

        return jsonify({
            "jobRunID": request.json.get("id", ""),
            "data": metal_prices
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sxbx_price', methods=['GET'])
def get_sxbx_price():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            return jsonify({"error": "Metal API error"}), 500

        data = response.json()

        # Gauta metalo kaina už unciją
        gold_price_per_oz = data["rates"]["USDXAU"]
        silver_price_per_oz = data["rates"]["USDXAG"]
        platinum_price_per_oz = data["rates"]["USDXPT"]
        palladium_price_per_oz = data["rates"]["USDXPD"]

        # Konvertuojame į USD už gramą (1 uncija = 31.1035 gramai)
        gold_price = gold_price_per_oz / 31.1035
        silver_price = silver_price_per_oz / 31.1035
        platinum_price = platinum_price_per_oz / 31.1035
        palladium_price = palladium_price_per_oz / 31.1035

        # SXBX mišinio proporcijos
        mix_price_per_gram = (
            (gold_price * 0.60) +
            (silver_price * 0.25) +
            (platinum_price * 0.10) +
            (palladium_price * 0.05)
        )

        # 1 SXBX = 0.025 g mišinio
        sxbx_price = mix_price_per_gram * 0.025

        return jsonify({"sxbx_price": round(sxbx_price, 4)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
