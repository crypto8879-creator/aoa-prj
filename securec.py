from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature


# 1. RSA Key Generation (generate_keys.py)
s_private = rsa.generate_private_key(65537, 2048)
r_private = rsa.generate_private_key(65537, 2048)

with open("sender_private.pem", "wb") as f:
    f.write(s_private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))

with open("sender_public.pem", "wb") as f:
    f.write(s_private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

with open("receiver_private.pem", "wb") as f:
    f.write(r_private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))

with open("receiver_public.pem", "wb") as f:
    f.write(r_private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

print("RSA Key Pairs Generated and Saved!")


# 2. Message Encryption & Digital Signing (sender.py)
with open("receiver_public.pem", "rb") as f:
    r_pub = serialization.load_pem_public_key(f.read())

with open("sender_private.pem", "rb") as f:
    s_priv = serialization.load_pem_private_key(f.read(), password=None)

msg = input("Enter message: ").encode("utf-8")

encrypted = r_pub.encrypt(
    msg,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

signature = s_priv.sign(
    msg,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

with open("encrypted_message.bin", "wb") as f:
    f.write(encrypted)

with open("signature.bin", "wb") as f:
    f.write(signature)

print("Message Encrypted and Signed!")


# 3. Message Decryption & Signature Verification (receiver.py)
with open("receiver_private.pem", "rb") as f:
    r_priv = serialization.load_pem_private_key(f.read(), password=None)

with open("sender_public.pem", "rb") as f:
    s_pub = serialization.load_pem_public_key(f.read())

with open("encrypted_message.bin", "rb") as f:
    encrypted = f.read()

with open("signature.bin", "rb") as f:
    signature = f.read()

decrypted = r_priv.decrypt(
    encrypted,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print("Decrypted Message:", decrypted.decode("utf-8"))

choice = input("Tamper message? (y/n): ").strip().lower()
msg_to_verify = input("Enter altered message: ").encode("utf-8") if choice == 'y' else decrypted

try:
    s_pub.verify(
        signature,
        msg_to_verify,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("Signature Verified: Authentic & Untampered!")
except InvalidSignature:
    print("SECURITY ALERT: Signature Verification Failed! Tampering Detected!")