from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ACTIVECAMPAIGN_URL = "https://focaleducacao.api-us1.com/api/7/contact/sync"
API_TOKEN = "64c44ed8a7b709307ca8fa039affc5d659e275e55cde3c03ec2df93d45a63269cfea1c52"

@app.route('/save-lead', methods=['POST'])
def submit_form():
    data = request.form
    headers = {
        'Api-Token': API_TOKEN,
        'Content-Type': 'application/json'
    }

    contact_data = {
        'contact': {
            'email': data.get('email'),
            'name': data.get('name'),
            'telefone': data.get('telefone')
        }
    }

    response = requests.post(ACTIVECAMPAIGN_URL, headers=headers, json=contact_data)

    if response.status_code == 200 or response.status_code == 201:
        return redirect('https://focaleducacao.com.br/obrigado-captura', code=302)
    else:
        return redirect('https://focaleducacao.com.br/erro-captura', code=302)

if __name__ == '__main__':
    app.run(debug=True)
