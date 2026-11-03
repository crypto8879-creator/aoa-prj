import hashlib

data = "This is important"
hash1 = hashlib.sha256(data.encode()).hexdigest()

tampered = "This is important"
hash2 = hashlib.sha256(tampered.encode()).hexdigest()

print("Hash1:", hash1)
print("Hash2:", hash2)
print("Integrity Verified?", hash1 == hash2)