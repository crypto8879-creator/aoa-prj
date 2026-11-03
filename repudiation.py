import hashlib

message = "Approve $5000 transfer"
signature = hashlib.sha256(message.encode()).hexdigest()

received_message = "Approve $5000 transfer"
received_signature = hashlib.sha256(received_message.encode()).hexdigest()

print("Signature Verified:", signature == received_signature)