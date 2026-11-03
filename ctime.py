#py -m pip install flask
#create a folder my project containing two files
#prac6.py
#sample.txt
#Time-Limited Secure File Access Demo (Flask Based)
# Download file
from flask import Flask, send_file
import time

app = Flask(__name__)
start = time.time()

@app.route('/')
def home():
    return '<h2>Secure File Access</h2><a href="/download">Download Secret File</a>'

@app.route('/download')
def download():
    if time.time() - start < 20:
        return send_file("backup_data.txt", as_attachment=True)
    else:
        return "Access Denied! Time Expired."

app.run()
