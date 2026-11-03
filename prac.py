from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

data = "Confidential Information"

encrypted_data = cipher.encrypt(data.encode())
decrypted_data = cipher.decrypt(encrypted_data).decode()

print("Encrypted data:", encrypted_data)
print("Decrypted data:", decrypted_data)