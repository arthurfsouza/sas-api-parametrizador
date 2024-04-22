import requests
import json


class RequestSID:
    def __init__(self, base_url, token, decision_name, entry_json) -> None:
        # Classe para criar chamadas aos fluxos publicados no SID
        self._base_url = base_url
        self._token = token
        self._decision_name = decision_name
        self._entry_json = entry_json
        self._sid_response = None
        self._sid_status = 400

    def _prepare_json(self, sid_response):
        """Funcao que transforma o response do SID em um json e adiciona os headers passados para o tradutor"""
        prepared_response = {}

        if sid_response.get("outputs"):
            for output in sid_response.get("outputs"):
                prepared_response[output.get("name")] = output.get("value")
        else:
            return sid_response

        return prepared_response

    def _call_decision(self):
        # Cria chamada para o fluxo passado em decision_name
        # As variáveis devem ser passadas para o entryJson_

        if self._token:
            urlSID = f"{self._base_url}/microanalyticScore/modules/{self._decision_name}/steps/execute"

            headersSID = {
                "Content-Type": "application/json;charset=utf-8",
                "Accept": "application/json",
                "Authorization": "Bearer " + self._token
            }

            bodySID = {
                "inputs":
                    [
                        {
                            "name": "entry_json_",
                            "value": self._entry_json
                        }
                    ]
            }

            try:
                response = requests.post(
                    urlSID,
                    data=json.dumps(bodySID, ensure_ascii=False),
                    headers=headersSID,
                    verify=False,
                    timeout=20
                )

                self._sid_response = self._prepare_json(response.json())
                self._sid_status = response.status_code

            except requests.exceptions.RequestException as e:
                self._sid_response = e
        else:
            self._sid_response = "Erro no token: não foi possível realizar a chamada"

    def check_decision_name(self, decision_name_list):
        check = True if self._decision_name in decision_name_list else False

        return check

    def return_sid(self):
        self._call_decision()

        # print(f"sid_response {self._sid_response}")
        # print(f"sid_status {self._sid_status}")

        return (self._sid_response, self._sid_status)