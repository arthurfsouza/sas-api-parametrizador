import json

''' List all output parameters as comma-separated values in the "Output:" docString. Do not specify "None" if there is no output parameter. ''' # noqa
def execute(entry_json):
    'Output:name, phone_num, email, comment, status_code, status_message'
    j = json.loads(entry_json)

    if ("name" in j) and ("email" in j) and ("comment" in j):
        name = j["name"]
        phone_num = j["phone_num"]
        email = j["email"]
        comment = j["comment"]

        status_code = 200
        status_message = ""

    else:
        name = ""
        phone_num = ""
        email = ""
        comment = ""

        status_code = 500
        status_message = "name, email or comment not found in entry_json."

    return name, phone_num, email, comment, status_code, status_message