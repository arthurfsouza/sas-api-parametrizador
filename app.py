import json
import logging
from flask import Flask, render_template, request, jsonify, logging as flog
from flask_cors import CORS

from resources.request_token import RequestToken
from resources.request_sid import RequestSID
from resources.request_folder import RequestFOLDER

app = Flask(__name__, template_folder="./templates")
CORS(app)
app.config["JSON_AS_ASCII"] = False

def logging_config(req_id=""):
    """Funcao responsavel por configurar o log da aplicacao"""

    flog.default_handler.setFormatter(logging.Formatter("%(message)s"))

    logging.basicConfig(
        level = "INFO",
        format = f"%(asctime)s - %(levelname)s : %(message)s",
        datefmt = "[%d/%b/%y - %H:%M:%S]",
        force = True
    )

    logging.info(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

@app.route("/api-sas", methods=["GET", "POST"])
def index():
    logging_config()

    if request.method == "GET":
        base_url = "https://rmdemo.unx.sas.com"
        username = "demo66"; password = "Go4thsas"

        request_tk = RequestToken(base_url, username, password, by_user=True)
        tk_response, tk_status = request_tk.return_token()

        logging.info(f"TOKEN status: {tk_status}")
        logging.info(f"TOKEN response: {tk_response}")

        if not tk_response or tk_status != 200:
            logging.info(f"could not create tk_response entity!")
            return jsonify({"token_status": tk_status, "token_response": tk_response}) #criar uma pagina pra esse erro

        request_folder = RequestFOLDER(base_url, tk_response, 100)
        folder_response, folder_status = request_folder.return_folder()

        logging.info(f"FOLDER status: {folder_status}")
        logging.info(f"FOLDER response: {folder_response}")

        return jsonify({"folder_status": folder_status, "folder_response": folder_response})

# @app.route("/", methods=["GET", "POST"])
# def index():
#     logging_config()

#     if request.method == "POST":
#         name = request.form["nome"]
#         phone_num = request.form["numero"]
#         email = request.form["email"]
#         comment = request.form["comentario"]

#         logging.info(f"comment: {comment}")

#         base_url = "http://13.90.73.61"
#         username = "ci_client_2"; password = "Orion123"

#         request_tk = RequestToken(base_url, username, password, by_user=False)
#         tk_response, tk_status = request_tk.return_token()

#         logging.info(f"TOKEN status: {tk_status}")
#         logging.info(f"TOKEN response: {tk_response}")

#         if not tk_response or tk_status != 200:
#             logging.info(f"could not create tk_response entity!")
#             return jsonify({"token_status": tk_status, "token_response": tk_response}) #criar uma pagina pra esse erro

#         decision_name = "sentiment_analysis_decision"

#         entry_json = {
#             "name": name,
#             "phone_num": phone_num,
#             "email": email,
#             "comment": comment
#         }

#         request_sid = RequestSID(base_url, tk_response, decision_name, json.dumps(entry_json))
#         sid_response, sid_status = request_sid.return_sid()

#         logging.info(f"base_url: {base_url}/microanalyticScore/modules/{decision_name}/steps/execute")
#         logging.info(f"SID status: {sid_status}")
#         logging.info(f"SID response: {sid_response}")

#         if not sid_response or sid_status != 201:
#             logging.info(f"could not create SID entity!")
#             return jsonify({"sid_status": sid_status, "sid_response": sid_response}) #criar uma pagina pra esse erro

#         # Retornar uma mensagem de confirmação para o usuário
#         return render_template("retorno.html", name=name, comment=sid_response.get("comment_score"))
#     elif request.method == "GET":
#         # Renderizar o template do formulário
#         return render_template("formulario.html")

if __name__ == "__main__":
    app.run(debug=True)