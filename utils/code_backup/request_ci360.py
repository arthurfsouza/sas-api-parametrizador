import requests
import json

''' List all output parameters as comma-separated values in the "Output:" docString. Do not specify "None" if there is no output parameter.'''
''' List all Python packages that are not built-in packages in the "DependentPackages:" docString. Separate the package names with commas on a single line. '''
''' DependentPackages: requests'''
def execute (name,phone_num,email,comment_score):
    'Output:status_message, status_code, ci_response'
    
    url = "https://extapigwservice-demo.cidemo.sas.com/marketingGateway/events"

    headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJRCI6IjQ3MDI5ZTcxY2IwMDAxM2QzNTFmZjJjMiJ9.Tnf5zDlrMBQzx2GvtHoP7QaToOfFrZETW5ywm0XP5p8"
    }

    payload = json.dumps({
      "eventName": "lucarm_sid_score",
      "login_id": "367.734.378-06",
      "sid_score": str(comment_score),
      "sid_celular": phone_num,
      "sid_email": email,
      "sid_nome": name
    })

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        status_code = response.status_code
        status_message = ""
        ci_response = str(response.json())

    except requests.exceptions.RequestException as e:
        status_code = 500
        status_message = "Request ci360 failed!"
        ci_response = f"{e}"

    return status_message, status_code, ci_response


result = execute(name="Antônio Vinicius", phone_num="61 984848484", email="asdf@gmail.com", comment_score=4.10)
print(result)
