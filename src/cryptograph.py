from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def encode(data: bin) -> tuple:
    with open('../keys/my_rsa_public.pem') as key:
        recipient_key = RSA.import_key(key.read())
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    return cipher_rsa.encrypt(session_key), cipher_aes.nonce, tag, ciphertext


def decode(inp: tuple):
    with open('../keys/my_private_rsa_key.bin') as key:
        private_key = RSA.import_key(key.read(), passphrase=open('../keys/passphrase.txt').read())
        enc_session_key, nonce, tag, ciphertext = inp
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data


if __name__ == '__main__':
    out = encode(b'hello world')
    print(out)
    print(decode(out))
