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