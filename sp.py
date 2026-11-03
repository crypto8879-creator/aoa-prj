#Demonstrate 2 different certificates producing the same md5 and hash

# Shortened Toy Hash: Sum of all characters modulo 256
toy_hash = lambda b: sum(b) % 256

# Two completely different plain-text certificates
cert1 = b"""-----BEGIN CERTIFICATE-----
Subject: CN=Alice Example

Issuer: Test CA
PublicKey: AAAAB3NzaC1yc2EAAAADAQABAAABAQCu
-----END CERTIFICATE-----
"""

cert2 = b"""-----BEGIN CERTIFICATE-----
Subject: CN=Bob Example
Issuer: Test CA
PublicKey: AAAAB3NzaC1yc2EAAAADAQABAAABAQCu
-----END CERTIFICATE-----
"""

# Calculate the exact single byte needed to make the hashes match
target_hash = toy_hash(cert1)
current_hash = toy_hash(cert2 + b"\n#PAD:")
needed_byte = (target_hash - current_hash) % 256

# Append the padding block to cert2
cert2_padded = cert2 + b"\n#PAD:" + bytes([needed_byte])

# Verify and print results
print(f"Cert 1 Hash       : {toy_hash(cert1)}")
print(f"Cert 2 Padded Hash: {toy_hash(cert2_padded)}")
print(f"Are bytes identical? : {cert1 == cert2_padded}")
print(f"Do they collide?     : {toy_hash(cert1) == toy_hash(cert2_padded)}")

# Save to disk
with open("cert1_demo.pem", "wb") as f:
    f.write(cert1)

with open("cert2_demo_padded.pem", "wb") as f:
    f.write(cert2_padded)

print("Files saved successfully!")


#Combined code of hash,mac and hmac

import hashlib
import hmac

# HASH
def hash_demo(msg):
    print("\n1. SHA-256 HASH")

    changed_msg = msg.lower()

    hash1 = hashlib.sha256(msg.encode()).hexdigest()
    hash2 = hashlib.sha256(changed_msg.encode()).hexdigest()

    print("Message 1:", msg)
    print("Hash 1:", hash1)
    print("Message 2:", changed_msg)
    print("Hash 2:", hash2)
    print("Hashes different:", hash1 != hash2)


# SIMPLE MAC
def mac_demo(key, msg):
    print("\n2. SIMPLE MAC")

    mac = hashlib.sha256(key + msg).hexdigest()

    print("Message:", msg.decode())
    print("MAC:", mac)


# HMAC
def hmac_demo(key, msg):
    print("\n3. SECURE HMAC")

    secure_mac = hmac.new(key, msg, hashlib.sha256).hexdigest()

    print("Message:", msg.decode())
    print("HMAC:", secure_mac)


# MAIN PROGRAM
print("HASH, MAC AND HMAC")

text_message = "Hello Security Students"
secret_key = b"my_super_secret_key_123"
byte_message = b"Important Transaction: Send $500 to Bob"

hash_demo(text_message)
mac_demo(secret_key, byte_message)
hmac_demo(secret_key, byte_message)

