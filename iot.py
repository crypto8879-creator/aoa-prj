#AES encryption for IOT Sensor Data secure
#py -m pip install pycryptodome
from Crypto.Cipher import AES 
import base64 
# AES requires 16/24/32 byte key 
key = b"ThisIsA16ByteKey" 
cipher = AES.new(key, AES.MODE_EAX) 
# IoT sensor data (example: temperature) 
sensor_data = "Temperature: 28C" 
# Encrypt 
ciphertext, tag = cipher.encrypt_and_digest(sensor_data.encode())
nonce = cipher.nonce 
print("Encrypted Data:", base64.b64encode(ciphertext).decode()) # Decrypt 
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
decrypted_data = cipher_dec.decrypt(ciphertext).decode()
print("Decrypted Data:", decrypted_data)

#HMAC for data integrity to ensure data is not tampered
import hmac 
import hashlib 
# Secret key shared between IoT device and server 
secret_key = b"iot_secret_key" 
# IoT message 
message = b"Humidity: 70%" 
# Generate HMAC 
hmac_digest = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
print("Message:", message.decode()) 
print("Generated HMAC:", hmac_digest) 
# Receiver verification 
received_hmac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
if hmac.compare_digest(hmac_digest, received_hmac): 
 print(" Message is authentic") 
else: 
 print(" Message tampered!")
 
#Packet sniffing in IOT 
#py -m pip install scapy
from scapy.all import sniff

# Callback function to process each captured packet
#download npmap
def packet_callback(packet):

    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst

        print(f"[IP Packet] {src} -> {dst}")

        if packet.haslayer("Raw"):  # application data
            payload = packet["Raw"].load
            print("Payload:", payload)

print("Sniffing IoT traffic... Press Ctrl+C to stop")

# Capture 10 packets
sniff(prn=packet_callback, count=10)
#check packets on cmd to from path where you downloaded nmap
#py prac7.py


#MQTT Secure Communication using Mosquitto
#open cmd and write the following command
#py -m pip install paho-mqtt
#Download the Mosquitto certificate
#Open CMD or PowerShell and execute
#curl.exe -o C:\Users\Prachi\Downloads\mosquitto.org.crt https://test.mosquitto.org/ssl/mosquitto.org.crt
#open cmd and execute py prac.py
import time
import paho.mqtt.client as mqtt

# Connect function
def on_connect(client, userdata, flags, rc, properties):
    print("Connected successfully")
    client.subscribe("iot/device1")

# Receive message
def on_message(client, userdata, msg):
    print("Received:", msg.payload.decode())

# Create client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

# Load certificate
client.tls_set(ca_certs="mosquitto.org.crt")

# Connect to MQTT server
client.connect("test.mosquitto.org", 8883, 60)

client.loop_start()

time.sleep(2)

# Send message
client.publish("iot/device1", "Temperature: 25C")

print("Message sent")

time.sleep(2)

client.loop_stop()
client.disconnect()

