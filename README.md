
# Cogna Sentiment Analysis

## Pré-requisitos:

1. Certifique-se de ter o Python instalado no seu sistema. Você pode baixá-lo em [python.org](https://www.python.org).
3. Instale o Flask e as dependências necessárias. Você pode fazer isso usando o pip, o gerenciador de pacotes do Python.

## Executando o Código:

1. **Preparação do Ambiente**:
    - Abra um terminal ou prompt de comando.
    - Navegue até o diretório onde está localizado o arquivo `app.py`.

2. **Executando o Aplicativo**:
    - Execute o arquivo `app.py` usando o Python.

3. **Acessando o Aplicativo**:
    - Após executar o comando acima, o Flask irá iniciar o servidor e o aplicativo estará disponível localmente.
    - Abra um navegador da web e acesse o endereço [http://localhost:5000](http://localhost:5000) para acessar o aplicativo.

4. **Interagindo com o Aplicativo**:
    - Na página inicial, você verá um formulário.
    - Preencha os campos do formulário (`nome`, `numero`, `email`, `comentario`) e envie o formulário.
    - O aplicativo processará os dados enviados, fará uma solicitação para obter um token e, em seguida, uma solicitação ao SID para realizar a análise de sentimento.
    - Se tudo correr conforme o esperado, você será redirecionado para uma página de confirmação onde é possível visualizar o resultado da análise de sentimento.

## Observações:

- Certifique-se de que o servidor Flask está em execução enquanto você interage com o aplicativo no navegador. Se você fechar o terminal ou o prompt de comando onde o Flask está sendo executado, o servidor também será encerrado e o aplicativo não estará mais acessível.
- Se você encontrar algum erro ao executar o código ou acessar o aplicativo, verifique se todas as dependências estão instaladas corretamente e se não há erros no código-fonte fornecido.
