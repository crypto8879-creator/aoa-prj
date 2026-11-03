import datetime

def log_action(user, action):
    with open("audit_log.txt", "a") as log:
        timestamp = datetime.datetime.now()
        log.write(f"{timestamp} - {user}: {action}\n")

log_action("admin", "Logged In")
log_action("user1", "Viewed Report")