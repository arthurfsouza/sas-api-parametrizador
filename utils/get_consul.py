''' List all output parameters as comma-separated values in the "Output:" docString. Do not specify "None" if there is no output parameter. '''
def execute ():
   'Output:consul'
   try:
        # Abre o arquivo em modo de leitura
        with open('/opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token', 'r') as file:
            # Lê o conteúdo do arquivo
            consul = file.read().strip()
            return consul
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retorna None
        return "Nao foi possivel localizar"
