import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency'] 
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    
    # Get just string without quotes 
    target_currency = data['queryResult']['parameters']['currency-name'][0]

    cf = fetch_conversion_factor(source_currency, target_currency)
    
    if cf is None:
        response = {
            "fulfillmentText": "Sorry, unable to get conversion rate."
        }
        return jsonify(response)
        
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    
    response = {
        "fulfillmentText": "{} {} is {} {}".format(amount, source_currency, 
                                                   final_amount, target_currency)
    }
    
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://api.currencyapi.com/v3/latest?apikey=cur_live_VoU1Ro2RWlOiNlLBFzENbaNoJ4NVgejSiT8o8tHs&currencies={}&base_currency={}".format(target, source)
    response = requests.get(url)
    data = response.json()
    
    try:
        return data['data'][target]['value']
    except KeyError:
        return None

if __name__ == "__main__":
    app.run(debug=True)
