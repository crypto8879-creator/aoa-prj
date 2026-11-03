
# FILE 1: user_auth.py (Run 1st: initializes DB and creates user)

import hashlib
import os
import secrets
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, salt TEXT, password_hash TEXT)"
    )
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hash_val = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return salt, hash_val.hex()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    salt, pwd_hash = hash_password(password)
    try:
        conn.execute("INSERT INTO users VALUES (?, ?, ?)", (username, salt, pwd_hash))
        conn.commit()
        return "User registered successfully!"
    except sqlite3.IntegrityError:
        return "Username already exists!"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    res = conn.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if not res:
        return False
    return hash_password(password, res[0])[1] == res[1]

if __name__ == "__main__":
    init_db()
    print(register_user("alice", "secret_password"))
    print("Current folder where users.db is saved:", os.path.abspath("users.db"))


# FILE replay 2A: server.py (Run 2nd: start this before lient.py)

import socket
from datetime import datetime, timedelta, timezone

# from user_auth import init_db, authenticate_user
#user_auth required

def run_replay_server():
    init_db()
    last_timestamp = None
    window = timedelta(seconds=30)

    server = socket.socket()
    server.bind(("localhost", 9999))
    server.listen(1)
    print("Server listening on port 9999...")

    conn, _ = server.accept()
    u, p = conn.recv(1024).decode(), conn.recv(1024).decode()

    if authenticate_user(u, p):
        conn.send(b"AUTH_OK")
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            msg, ts_str = data.split("||")
            msg_time = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)

            if last_timestamp and msg_time <= last_timestamp:
                resp = "Replay attack detected: Old timestamp."
            elif abs(now - msg_time) > window:
                resp = "Timestamp expired."
            else:
                last_timestamp = msg_time
                resp = "Timestamp valid."

            print(f"[{u}] {msg} => {resp}")
            conn.send(resp.encode())
    else:
        conn.send(b"AUTH_FAILED")

    conn.close()
    server.close()

if __name__ == "__main__":
    run_replay_server()


# FILE 2B: client.py (Run 3rd: run after server.py is listening)

import socket
import time
from datetime import datetime, timezone

def run_replay_client():
    client = socket.socket()
    client.connect(("localhost", 9999))

    client.send(b"alice")
    time.sleep(0.5)
    client.send(b"secret_password")

    if client.recv(1024) == b"AUTH_OK":
        print("Logged in!")
        msg = "Transfer $100"
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        payload = f"{msg}||{ts}"

        # Send Original
        client.send(payload.encode())
        print("Server:", client.recv(1024).decode())

        # Simulate Replay Attack
        time.sleep(2)
        print("\n[Replaying same message...]")
        client.send(payload.encode())
        print("Server:", client.recv(1024).decode())

    client.close()

if __name__ == "__main__":
    run_replay_client()


# FILE encrypted file transfer 3A: secure_server.py (Run 4th: start this before running secure_client.py)

import socket
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# from user_auth import authenticate_user

AES_KEY = bytes.fromhex("054f0c5c692ffa3e0d0fa7d156966812")

def run_secure_file_server():
    aesgcm = AESGCM(AES_KEY)
    server = socket.socket()
    server.bind(("localhost", 8888))
    server.listen(1)
    print("File Server on 8888...")

    conn, _ = server.accept()
    u, p = conn.recv(1024).decode(), conn.recv(1024).decode()

    if authenticate_user(u, p):
        conn.send(b"AUTH_OK")
        nonce = conn.recv(12)
        fname = conn.recv(1024).decode()
        fsize = int(conn.recv(1024).decode())

        enc_data = b""
        while len(enc_data) < fsize:
            enc_data += conn.recv(4096)

        try:
            decrypted = aesgcm.decrypt(nonce, enc_data, None)
            with open("received_" + fname, "wb") as f:
                f.write(decrypted)
            conn.send(b"File received and decrypted.")
        except Exception:
            conn.send(b"Decryption/Integrity check failed.")
    else:
        conn.send(b"AUTH_FAILED")

    conn.close()
    server.close()

if __name__ == "__main__":
    run_secure_file_server()


# FILE 3B: secure_client.py (Run 5th: run after secure_server.py is listening)

import os
import socket
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AES_KEY = bytes.fromhex("054f0c5c692ffa3e0d0fa7d156966812")

def run_secure_file_client():
    aesgcm = AESGCM(AES_KEY)
    client = socket.socket()
    client.connect(("localhost", 8888))

    client.send(b"alice")
    time.sleep(0.5)
    client.send(b"secret_password")

    if client.recv(1024) == b"AUTH_OK":
        if not os.path.exists("sample.txt"):
            with open("sample.txt", "wb") as f:
                f.write(b"Confidential payload: authenticated file transfer test.")

        with open("sample.txt", "rb") as f:
            file_data = f.read()

        nonce = os.urandom(12)
        enc_data = aesgcm.encrypt(nonce, file_data, None)

        client.send(nonce)
        time.sleep(0.1)
        client.send(b"sample.txt")
        time.sleep(0.1)
        client.send(str(len(enc_data)).encode())
        time.sleep(0.1)
        client.sendall(enc_data)

        print("Server:", client.recv(1024).decode())

    client.close()

if __name__ == "__main__":
    run_secure_file_client()

