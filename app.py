from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ACTIVECAMPAIGN_BASE_URL = "https://focaleducacao.api-us1.com/api/3"
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
        return redirect('https://focaleducacao.com.br/erro-captura', code=301)

    contact_id = response.json().get('contact').get('id')

    # Em seguida, adicione o contato à lista com ID 7
    list_data = {
        'contactList': {
            'list': 7,
            'contact': contact_id,
            'status': 1  # 1 para adicionar à lista
        }
    }

    response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contactLists", headers=headers, json=list_data)
    print(response.text)

    if response.status_code in [200, 201]:
        return redirect('https://focaleducacao.com.br/obrigado-captura', code=302)
    else:
        return redirect('https://focaleducacao.com.br/erro-captura', code=301)

if __name__ == '__main__':
    app.run(debug=True)
