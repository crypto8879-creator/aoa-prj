
from cryptography.fernet import Fernet
import os
import shutil

# Create cloud folder
os.makedirs("cloud_backup", exist_ok=True)

# Generate AES key
key = Fernet.generate_key()

# Save AES key
with open("aes.key", "wb") as f:
    f.write(key)

fernet = Fernet(key)

# Create sample file if not present
if not os.path.exists("sample_file.txt"):
    with open("sample_file.txt", "w") as f:
        f.write("Confidential Cloud Backup File")

# Read and encrypt file
with open("sample_file.txt", "rb") as f:
    data = f.read()

encrypted = fernet.encrypt(data)

# Save encrypted file
with open("enc_sample_file.txt", "wb") as f:
    f.write(encrypted)

# Copy encrypted file to cloud folder
shutil.copy("enc_sample_file.txt", "cloud_backup")

print("Encrypted and uploaded: enc_sample_file.txt")
print("AES Key generated: aes.key")
print("Cloud backup folder created successfully!")
