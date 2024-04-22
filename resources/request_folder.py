import requests
import json

class RequestFOLDER:
    def __init__(self, base_url, token, limit) -> None:
        # Classe para criar chamadas aos fluxos publicados no FOLDER
        self._base_url = base_url
        self._token = token
        self._limit = limit
        self._folder_response = None
        self._folder_status = 400

    def _prepare_json(self, folder_response):
        """Funcao que transforma o response do FOLDER em um json e adiciona os headers passados para o tradutor"""
        prepared_response = {}

        if folder_response.get("outputs"):
            for output in folder_response.get("outputs"):
                prepared_response[output.get("name")] = output.get("value")
        else:
            return folder_response

        return prepared_response

    def _call_folder(self):
        # Cria chamada para o fluxo passado

        if self._token:
            urlFOLDER = f"{self._base_url}/folders/folders?limit={self._limit}"

            headersFOLDER = {
                "Content-Type": "application/json;charset=utf-8",
                "Accept": "application/json",
                "Authorization": "Bearer " + self._token
            }

            try:
                response = requests.get(
                    urlFOLDER,
                    headers=headersFOLDER,
                    verify=False,
                    timeout=20
                )

                self._folder_response = self._prepare_json(response.json())
                self._folder_status = response.status_code

            except requests.exceptions.RequestException as e:
                self._folder_response = e
        else:
            self._folder_response = "Erro no token: não foi possível realizar a chamada"

    def return_folder(self):
        self._call_folder()

        # print(f"_folder_response {self._folder_response}")
        # print(f"_folder_status {self._folder_status}")

        return (self._folder_response, self._folder_status)