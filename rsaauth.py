import socket
import secrets
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa



# FILE 1: generate_rsa_keys.py
def step1_generate_keys():
    key = rsa.generate_private_key(65537, 2048)

    with open("client_private.pem", "wb") as f:
        f.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )

    with open("client_public.pem", "wb") as f:
        f.write(
            key.public_key().public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    print("RSA Keys generated and saved!")



# FILE 2: rsa_server.py
def step2_run_server():
    with open("client_public.pem", "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())

    server = socket.socket()
    server.bind(("localhost", 7777))
    server.listen(1)
    print("RSA Server running on 7777... Waiting for client...")

    conn, addr = server.accept()
    challenge = secrets.token_bytes(32)
    conn.send(challenge)

    signature = conn.recv(512)
    try:
        pub_key.verify(signature, challenge, padding.PKCS1v15(), hashes.SHA256())
        conn.send(b"AUTH_OK")
        print("Authentication Successful!")
    except Exception:
        conn.send(b"AUTH_FAILED")
        print("Authentication Failed!")

    conn.close()
    server.close()



# FILE 3: rsa_client.py

def step3_run_client():
    with open("client_private.pem", "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=None)

    client = socket.socket()
    client.connect(("localhost", 7777))

    challenge = client.recv(1024)
    signature = priv_key.sign(challenge, padding.PKCS1v15(), hashes.SHA256())
    client.send(signature)

    response = client.recv(1024).decode()
    print("Server response:", response)

    client.close()


# First run this:
step1_generate_keys()

# step2_run_server()

# step3_run_client()