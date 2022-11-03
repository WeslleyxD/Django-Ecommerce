import json
import requests

def via_cep(cep):
    r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    response = json.loads(r.text)

    response = response.get('erro')

    if not response:
        return r.text
    else:
        return False