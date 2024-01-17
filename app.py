from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#Nao alterar URL abaixo, significa versao 3 da api do active
ACTIVECAMPAIGN_BASE_URL = "https://seusubdominio.api-us1.com/api/3"
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
            'firstName': data.get('primeiroNome'),  # Ajustado para 'primeiroNome'
            'email': data.get('email'),
            'phone': data.get('telefone'),
            'fieldValues': [
                {'field': '1', 'value': data.get('AV0124_UTM_SOURCE')},
                {'field': '3', 'value': data.get('AV0124_UTM_MEDIUM')},
                {'field': '4', 'value': data.get('AV0124_UTM_CAMPAIGN')},
                {'field': '5', 'value': data.get('AV0124_UTM_CONTENT')},
                {'field': '6', 'value': data.get('AV0124_UTM_TERM')}
            ]
        }
    }

    # Primeiro, sincronize (crie/atualize) o contato
    response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contact/sync", headers=headers, json=contact_data)
    if response.status_code not in [200, 201]:
        print("Erro ao sincronizar contato:", response.text)
        return jsonify({"message": "Erro ao salvar lead"}), 400

    contact_id = response.json().get('contact', {}).get('id')

    # Se não houve erro, adicione o contato à lista com ID 2
    if contact_id:
        list_data = {
            'contactList': {
                'list': 2,  # ID da lista para a qual você quer adicionar o contato
                'contact': contact_id,
                'status': 1  # Status '1' para adicionar o contato à lista
            }
        }

        response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contactLists", headers=headers, json=list_data)
        if response.status_code in [200, 201]:
            return jsonify({"message": "Lead salvo com sucesso"}), 200
        else:
            print("Erro ao adicionar contato à lista:", response.text)
            return jsonify({"message": "Erro ao adicionar contato à lista"}), 400
    else:
        return jsonify({"message": "ID do contato não encontrado"}), 400

if __name__ == '__main__':
    app.run(debug=True)
