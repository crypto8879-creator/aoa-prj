#pip install cryptography
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = "Top Secret Message!"
encrypted = cipher.encrypt(message.encode())
decrypted = cipher.decrypt(encrypted).decode()

print("Key:", key.decode())
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)