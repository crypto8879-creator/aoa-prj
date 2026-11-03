#make json file abc.json
#import json
from datetime import datetime

# Set your blacklisted IPs
blacklisted_ips = ["192.168.1.10", "10.0.0.5"]

# Load access logs
with open("abc.json") as f:
    logs = json.load(f)

# Dictionary to count failed attempts
failed_attempts = {}

print("\nIntrusion Detection Log Analysis:\n")

for entry in logs:
    user = entry["user"]
    ip = entry["ip"]
    time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
    status = entry["status"]

    # Blacklist check
    if ip in blacklisted_ips:
        print(f"ALERT: Access from blacklisted IP {ip} by user '{user}'")

    # Time window check (office hours: 08:00 to 18:00)
    if not (8 <= time.hour <= 18):
        print(f"Off-hour login attempt by '{user}' at {time.strftime('%H:%M')}")

    # Failed login tracking
    if status == "failed":
        failed_attempts[user] = failed_attempts.get(user, 0) + 1

        if failed_attempts[user] >= 2:
            print(f"User '{user}' has {failed_attempts[user]} failed login attempts!")

print("\nLog scan completed.\n")
