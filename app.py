from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ACTIVECAMPAIGN_BASE_URL = "https://febracis65440.api-us1.com/api/3"
API_TOKEN = "c383bbd6bec55c9932f1f94ecb3580c9f1bba25d8c56e2ed2001501af161a81a6a3cb2ed"

@app.route('/test', methods=['POST'])
def test():
    return "testado"

@app.route('/save-lead', methods=['POST'])
def submit_form():
    # Usar request.form em vez de request.json para dados x-www-form-urlencoded
    data = request.form
    headers = {
        'Api-Token': API_TOKEN,
        'Content-Type': 'application/json'
    }

    # Certifique-se de que os nomes dos campos correspondam exatamente aos nomes usados no cURL
    contact_data = {
        'contact': {
            'firstName': data.get('primeiroNome'),
            'email': data.get('email'),
            'phone': data.get('telefone'),
            'fieldValues': [
                {'field': 'AV0124_UTM_SOURCE', 'value': data.get('AV0124_UTM_SOURCE')},
                {'field': 'AV0124_UTM_MEDIUM', 'value': data.get('AV0124_UTM_MEDIUM')},
                {'field': 'AV0124_UTM_CAMPAIGN', 'value': data.get('AV0124_UTM_CAMPAIGN')},
                {'field': 'AV0124_UTM_CONTENT', 'value': data.get('AV0124_UTM_CONTENT')},
                {'field': 'AV0124_UTM_TERM', 'value': data.get('AV0124_UTM_TERM')}
            ]
        }
    }

    # Realize a solicitação POST para sincronizar o contato
    response = requests.post(f"{ACTIVECAMPAIGN_BASE_URL}/contact/sync", headers=headers, json=contact_data)
    if response.status_code not in [200, 201]:
        print("Erro ao sincronizar contato:", response.text)
        return jsonify({"message": "Erro ao salvar lead"}), 400

    contact_id = response.json().get('contact', {}).get('id')

    # Verifique se contact_id foi obtido com sucesso antes de prosseguir
    if not contact_id:
        return jsonify({"message": "Erro ao obter ID do contato"}), 400

    # Adicione o contato à lista, se necessário
    # ... (a parte de adicionar à lista pode permanecer igual) ...

    return jsonify({"message": "Lead salvo com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)
