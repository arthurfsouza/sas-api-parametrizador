#https://developer.sas.com/apis/rest/CoreServices/#operations-7
#https://developer.sas.com/reference/auth/#register

import requests
import json

# cat /opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token
# kubectl --kubeconfig=/export/viya4-terraform/cliente360-dev-aks-kubeconfig.conf  -n viya4 get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)" #34b53f67-a46f-11ec-9a58-06a12280b569
# /green/viya4-green-kubernetes/kubectl --kubeconfig=/green/viya4-green-terraform/green-360-aks-kubeconfig.conf -n viya4-green get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)" # f1347977-ec11-11ec-bf4e-cee09fd591e4
# /blue/viya4-blue-kubernetes/kubectl --kubeconfig=/blue/viya4-blue-terraform/blue-360-aks-kubeconfig.conf -n viya4-blue get secret sas-consul-client -o jsonpath="{.data.CONSUL_TOKEN}" | echo "$(base64 -d)" # b2133d7f-e751-11ec-abb1-6242bcfe85bc

consul = 'b2133d7f-e751-11ec-abb1-6242bcfe85bc'

baseUrl = "https://cliente360blue.intranet"
client_id = "" # client_id that you are creating
client_secret = "" # client_secret for the client you are creating

# Get the SAS Viya Consul token to register a new client
urlTokenConsul = baseUrl + "/SASLogon/oauth/clients/consul?callback=false&serviceId=app"
tokenFinal = ''
headers = {"X-Consul-Token": consul}

try:
    firstToken = requests.post(urlTokenConsul, headers=headers, verify=False).json()["access_token"]
except requests.exceptions.RequestException as e:
    print(e)

print(f"firstToken {firstToken}")

# Register the new client
urlTokenClients = baseUrl + "/SASLogon/oauth/clients"
headersClients = {
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + firstToken
}
bodyClients = {
    "client_id": client_id, 
    "client_secret": client_secret, 
    "scope": ["openid"],
    "authorized_grant_types": ["client_credentials", "refresh_token"],
    "access_token_validity": 43200,
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob"}

try:
    secToken = requests.post(urlTokenClients, data=json.dumps(bodyClients), headers=headersClients, verify=False)
except requests.exceptions.RequestException as e:
    print("Error")
    print(e)

print(secToken)
print(secToken.text)

# curl -X POST --insecure "https://cliente360hml.intranet/SASLogon/oauth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=password&username=TR461006&password=ZofLotg37flEC5R" -u "TR461006:ZofLotg37flEC5R"
# curl -k -X POST --insecure "https://cliente360hml.intranet/SASLogon/oauth/token" -H "Accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=authorization_code&code=rPhSNl9K6c" -u "TR461006:ZofLotg37flEC5R"
# curl -k -X POST --insecure "https://cliente360hml.intranet/SASLogon/oauth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials" -u "TR461006:ZofLotg37flEC5R"