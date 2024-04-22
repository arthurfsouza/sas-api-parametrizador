1) Instalar o Git
2) Instalar o NGinx (descompactalo após o download)
3) Instalar bibliotecas do Python:
- 3.1) python -m pip install requests
- 3.2) pyhton -m pip install flask
- 3.3) pyhton -m pip install flask-cors
4) Criar um diretório para colocar os arquivos do projeto
5) Baixar o projeto do meu GIT pessoal no diretório criado anteriormente
- 4.1) git clone https://github.com/arthurfsouza/sas-api-parametrizador.git
6) Navegar através do prompt para a pasta "sas-api-parametrizador" criada através do passo anterioir
7) Copiar o arquivo "browzer.zip" (descompactado) localizado em "angular-build" para a pasta "html" do NGinx
8) Editar o arquivo "nginx.conf" da pasta "conf" do NGinx com:
- 8.1)
	server {
        	listen       9090;
        	server_name  localhost;
		root   html/browser;

		...

		location / {
			try_files $uri $uri/ /index.html;
        	}

		...
	}
9) executar o arquivo  "nginx.exe" dentro da pasta descompactada do NGinx para subir a aplicação web em localhost:9090
10) executar o comando "pyhton app.py" dentro da pasta do projeto baixado do GIT
11) Acessar no navegador o "https://rmdemo.unx.sas.com/SASVisualAnalytics/
12) Abrir o relatório "SAS-Parametrizador" que utilizará um componente para abrir a aplicação web que está rodando localmente