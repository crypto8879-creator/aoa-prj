#py -m pip install flask
#create a folder my project containing two files
#prac6.py
#sample.txt
#make client_encrypted_backup.py
from cryptography.fernet import Fernet
import os
import shutil

# Create a simulated cloud folder
os.makedirs("cloud_backup", exist_ok=True)

# Step 1: Generate a secret key (AES)
key = Fernet.generate_key()
fernet = Fernet(key)

# Save the key securely (local file)
with open("aes.key", "wb") as kf:
    kf.write(key)

# Step 2: Encrypt the file
def encrypt_file(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    encrypted_file = "enc_" + os.path.basename(file_path)

    with open(encrypted_file, "wb") as ef:
        ef.write(encrypted_data)

    # Simulate cloud upload
    shutil.copy(encrypted_file, "cloud_backup")

    print(f"Encrypted and uploaded: {encrypted_file}")


# Step 3: Run the encryption
if __name__ == "__main__":

    input_file = "sample_file.txt"

    # Create file if not present
    if not os.path.exists(input_file):
        with open(input_file, "w") as f:
            f.write("Confidential Cloud Backup File")

    encrypt_file(input_file)
