import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=0'


class RequestToken:
    def __init__(self, baseUrl, username, password, by_user=True) -> None:
        self._baseUrl = baseUrl
        self._username = username
        self._password = password
        self._by_user = by_user
        self._token_response = None
        self._token_status = 400

    def _generate_token_by_user(self):
        # Cria uma primeira chamada ao SID para gerar um token de acesso
        urlToken = self._baseUrl + "/SASLogon/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password
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

            if response.status_code == 200:
                self._token_response = response.json()["access_token"]
                self._token_status = response.status_code
            else:
                self._token_response = response.json()
                self._token_status = response.status_code

        except requests.exceptions.RequestException as e:
            self._token_response = e

    def _generate_token_by_client(self):
        # Cria uma primeira chamada ao SID para gerar um token de acesso
        urlToken = self._baseUrl + "/SASLogon/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self._username,
            "client_secret": self._password
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
                self._token_response = response.json()["access_token"]
                self._token_status = response.status_code
            else:
                self._token_response = response.json()
                self._token_status = response.status_code

        except requests.exceptions.RequestException as e:
            self._token_response = e

    def return_token(self):
        if self._by_user:
            self._generate_token_by_user()
        else:
            self._generate_token_by_client()           

        # print(f"token_response {self._token_response}")
        # print(f"token_status {self._token_status}")

        return (self._token_response, self._token_status)


# if __name__ == "__main__":

#     request_token = requestToken(
#         baseUrl="https://cliente360hml.intranet",
#         username="",
#         password="",
#         by_user=False
#     )

#     print(f"request_token {request_token.return_token()}")
