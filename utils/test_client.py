import requests
import json

def generate_token_by_client(base_url, username, password):
    # Cria uma primeira chamada ao SID para gerar um token de acesso
    urlToken = base_url + "/SASLogon/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": username,
        "client_secret": password
    }

    try:
        response = requests.post(
            urlToken,
            data=data,
            headers=headers,
            verify=False,
            timeout=20
        )

        if response.status_code == 200:
            token_response = response.json()["access_token"]
            token_status = response.status_code
        else:
            token_response = response.json()
            token_status = response.status_code

    except requests.exceptions.RequestException as e:
        token_response = e

    return token_response

def generate_token_by_user(base_url, username, password):
    # Cria uma primeira chamada ao SID para gerar um token de acesso
    urlToken = base_url + "/SASLogon/oauth/token"
    print(f"urlToken {urlToken}")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    authToken = ("sas.cli", "")

    try:
        response = requests.post(
            urlToken,
            data=data,
            headers=headers,
            verify=False,
            auth=authToken,
            timeout=20
        )

        print(f"response {response}")

        if response.status_code == 200:
            token_response = response.json()["access_token"]
            token_status = response.status_code
        else:
            token_response = response.json()
            token_status = response.status_code

    except requests.exceptions.RequestException as e:
        token_response = e

    return token_response


def aux(base_url, first_token, client_id, client_secret):
    # Register the new client
    urlTokenClients = base_url + "/SASLogon/oauth/clients"

    headersClients = {
        "Content-Type" : "application/json",
        "Authorization": "Bearer " + first_token
    }

    bodyClients = {
        "client_id": client_id, 
        "client_secret": client_secret, 
        "scope": ["openid"],
        "authorized_grant_types": ["client_credentials", "refresh_token"],
        "access_token_validity": 43200,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob"
    }

    try:
        secToken = requests.post(urlTokenClients, data=json.dumps(bodyClients), headers=headersClients, verify=False)
    except requests.exceptions.RequestException as e:
        print("Error")
        print(e)

    print(secToken)
    print(secToken.text)

def get_clients(token):
    headers = {
    'Accept': 'application/json',
    "Authorization": "Bearer " + token
    }

    r = requests.get('https://demoserver.internal.cloudapp.net/SASLogon/oauth/clients', headers = headers, verify = False)

    print(r.json())

base_url = "http://13.90.73.61"
username = "provuser01"
password = "Orion123"

token = generate_token_by_user(base_url, username, password)

# print(token)

base_url = "https://13.90.73.61"
client_id = "ci_client_2"
client_secret = "Orion123"
decision_name = "sentiment_analysis_decision_ci360"

aux(base_url, token, client_id, client_secret)

token = generate_token_by_client(base_url, client_id, client_secret)

print(token)

