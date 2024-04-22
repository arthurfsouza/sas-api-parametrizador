def decode_url_encoded_string(encoded_string):
    decoded_string = ""
    i = 0
    while i < len(encoded_string):
        if encoded_string[i] == '+':
            decoded_string += ' '
        elif encoded_string[i] == '%':
            decoded_string += chr(int(encoded_string[i+1:i+3], 16))
            i += 2
        else:
            decoded_string += encoded_string[i]
        i += 1
    return decoded_string

# Exemplo de uma string codificada
encoded_string = "exemplo+de+texto+com+espaos"

# Decodificar a string
decoded_string = decode_url_encoded_string(encoded_string)
print("String decodificada:", decoded_string)