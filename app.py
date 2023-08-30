from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

ACTIVECAMPAIGN_URL = "https://focaleducacao.api-us1.com/api/3/contact/sync"
API_TOKEN = "d364730c47f04bdd8a644e1be3b8f93acb302690c61d2793ae3b03212bb1aedbb2840101"

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
            'nome': data.get('nome'),
            'telefone': data.get('telefone')
        }
    }

    response = requests.post(ACTIVECAMPAIGN_URL, headers=headers, json=contact_data)

    if response.status_code == 200 or response.status_code == 201:
        return redirect('https://focaleducacao.com/obrigado-dominando-mercado', code=302)
    else:
        return redirect('https://focaleducacao.com/obrigado-dominando-mercado', code=302)

if __name__ == '__main__':
    app.run(debug=True)
