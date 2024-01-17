from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ACTIVECAMPAIGN_BASE_URL = "https://febracis65440.api-us1.com/"
API_TOKEN = "c383bbd6bec55c9932f1f94ecb3580c9f1bba25d8c56e2ed2001501af161a81a6a3cb2ed"

@app.route('/save-lead', methods=['POST'])
def submit_form():
    data = request.form
    headers = {
        'Api-Token': API_TOKEN,
        'Content-Type': 'application/json'
    }

    contact_data = {
        'contact': {
            'firstName': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('telefone'),
            'fieldValues': [
                {'field': '7', 'value': data.get('utm_source')},
                {'field': '8', 'value': data.get('utm_content')},
                {'field': '9', 'value': data.get('utm_medium')},
                {'field': '10', 'value': data.get('utm_term')},
                {'field': '11', 'value': data.get('utm_campaign')}
            ]
        }
    }

    # Primeiro, sincronize (crie/atualize) o contato
    response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contact/sync", headers=headers, json=contact_data)
    if response.status_code not in [200, 201]:
        print("Erro ao sincronizar contato:", response.text)
        return jsonify({"message": "Erro ao salvar lead"}), 400

    contact_id = response.json().get('contact').get('id')

    # Em seguida, adicione o contato à lista com ID 7
    list_data = {
        'contactList': {
            'list': 2,
            'contact': contact_id,
            'status': 1  # 1 para adicionar à lista
        }
    }

    response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contactLists", headers=headers, json=list_data)
    print(response.text)

    if response.status_code in [200, 201]:
        return jsonify({"message": "Lead salvo com sucesso"}), 200
    else:
        return jsonify({"message": "Erro ao salvar lead"}), 400

if __name__ == '__main__':
    app.run(debug=True)
