from Crypto.Cipher import AES
clave = b'cH~"PQeNYb^X&WcP>i[eh.]_RKs(_>,P' 

    # Crea un objeto cifrador AES
cipher = AES.new(clave, AES.MODE_ECB)
def main():
    
    encriptacion = encriptar("g$MlS=O+3O.*A'N&+2nW")
    desencripado = decrypt(encriptacion)
    return encriptacion

def encriptar(text):
    # Define la clave (debe tener 16, 24 o 32 bytes de longitud para AES-128, AES-192 o AES-256 respectivamente)
    
    # Define el texto a encriptar
    
    # Asegúrate de que el texto a encriptar tenga una longitud múltiplo de 16 bytes (tamaño del bloque de AES)
    texto_a_encriptar =  text.encode('utf-8')

    # Asegúrate de que el texto a encriptar tenga una longitud múltiplo de 16 bytes (tamaño del bloque de AES)
    longitud_texto = len(texto_a_encriptar)
    if longitud_texto % 16 != 0:
        texto_a_encriptar += b' ' * (16 - (longitud_texto % 16))

    # Encripta el texto
    texto_cifrado = cipher.encrypt(texto_a_encriptar)
    return texto_cifrado
def decrypt(text_encrypt):
    # Desencripta el texto cifrado
    texto_desencriptado = cipher.decrypt(text_encrypt)

    # Decodifica el texto desencriptado a una cadena
    texto_desencriptado = texto_desencriptado.strip().decode('utf-8')
    return texto_desencriptado
if __name__ == "__main__":
    resultado = main()
    print("Resultado de la encriptación:", resultado)