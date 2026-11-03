import hashlib
from cryptography.fernet import Fernet


# 1. User Authentication (Password Hashing)
users = {}

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def register(u, p):
    users[u] = hash_pass(p)

def login(u, p):
    return "Access Granted!" if users.get(u) == hash_pass(p) else "Access Denied!"

register("admin", "securepass")
print(login("admin", "securepass"))
print(login("admin", "wrongpass"))


# 2. Role-Based File Access (RBAC)
permissions = {
    "admin": ["read", "write"],
    "guest": ["read"]
}

def access_file(role, action):
    if action in permissions.get(role, []):
        print(f"{role} can {action} the file")
    else:
        print(f"{role} cannot {action} the file")

access_file("admin", "write")
access_file("guest", "write")


# 5. Basic IP Firewall Simulation
blocked_ips = ["192.168.1.100", "10.0.0.5"]

def check_access(ip):
    if ip in blocked_ips:
        print(f"Access Denied for {ip}")
    else:
        print(f"Access Granted for {ip}")

check_access("192.168.1.100")
check_access("8.8.8.8")


# 3. File Encryption with AES
key = Fernet.generate_key()
fernet = Fernet(key)

with open("example.txt", "w") as f:
    f.write("Secret OS Data")

with open("example.txt", "rb") as f:
    data = f.read()

with open("example.txt", "wb") as f:
    f.write(fernet.encrypt(data))

print("File Encrypted Successfully!")


# 4. File Integrity Checker (Anti-tamper)
def get_fhash(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

og_hash = get_fhash("example.txt")
curr_hash = get_fhash("example.txt")

print("File is intact" if og_hash == curr_hash else "File has been changed")


