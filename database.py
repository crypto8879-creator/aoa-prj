import sqlite3
import bcrypt
from cryptography.fernet import Fernet


# 1. Securing Database with Parameterized Queries (SQLi Prevention)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
cursor.execute("INSERT INTO users VALUES ('admin', 'admin_password')")

u = input("Enter username: ")
p = input("Enter password: ")

cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (u, p))
result = cursor.fetchone()

print("Login successful!" if result else "Invalid credentials!")


# 2. Encrypting Sensitive Data in Database (Bcrypt Hashing)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (username TEXT, password BLOB)")


u = input("Register username: ")
p = input("Register password: ")
hashed_p = bcrypt.hashpw(p.encode(), bcrypt.gensalt())
cursor.execute("INSERT INTO users VALUES (?, ?)", (u, hashed_p))


l_u = input("Login username: ")
l_p = input("Login password: ")
cursor.execute("SELECT password FROM users WHERE username = ?", (l_u,))
row = cursor.fetchone()

if row and bcrypt.checkpw(l_p.encode(), row[0]):
    print("Login successful!")
else:
    print("Login failed!")


# 3. Role-Based Access Control (RBAC) in Database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (username TEXT, password TEXT, role TEXT)")
cursor.execute("INSERT INTO users VALUES ('admin', 'admin_pwd', 'admin')")
cursor.execute("INSERT INTO users VALUES ('john', 'john_pwd', 'student')")

u = input("Enter username: ")
p = input("Enter password: ")

cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (u, p))
user = cursor.fetchone()

if user:
    role = user[0]
    print(f"Login successful! Role: {role}")
    if role == "admin":
        print("Access: View, Add, Delete, Modify records")
    elif role == "student":
        print("Access: View records only")
else:
    print("Invalid credentials!")



key = Fernet.generate_key()
cipher = Fernet(key)

data = "Confidential Information"

encrypted_data = cipher.encrypt(data.encode())
decrypted_data = cipher.decrypt(encrypted_data).decode()

print("Encrypted data:", encrypted_data)
print("Decrypted data:", decrypted_data)