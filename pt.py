#Port Scanning and Vulnerability
#scan_ports() – Finds open ports.
#grab_banner() – Gets service information.
#check_vulnerabilities() – Checks vulnerable software versions
import socket
from datetime import datetime

# Vulnerability database
vulnerabilities = {
    "Apache/2.2.8": "Outdated Apache version",
    "OpenSSH_4.7": "Old OpenSSH version",
    "Microsoft-IIS/6.0": "Outdated IIS version"
}

# Scan ports
def scan_ports(target, ports):
    open_ports = []

    print("\nScanning ports...")

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            print("Port", port, "is OPEN")
            open_ports.append(port)

        sock.close()

    return open_ports


# Get service banner
def grab_banner(target, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))

        banner = sock.recv(1024).decode().strip()
        sock.close()

        return banner

    except:
        return None


# Check vulnerabilities
def check_vulnerabilities(banner):
    for version in vulnerabilities:
        if version in banner:
            return vulnerabilities[version]

    return "No known vulnerability"


# Main program
if __name__ == "__main__":

    target = input("Enter Target IP: ")

    ports = [21, 22, 23, 25, 80, 110, 143, 443, 3389]

    start_time = datetime.now()

    open_ports = scan_ports(target, ports)

    print("\nBanner Checking")

    for port in open_ports:
        banner = grab_banner(target, port)

        if banner:
            print("\nPort:", port)
            print("Banner:", banner)
            print("Vulnerability:", check_vulnerabilities(banner))

        else:
            print("Port", port, "- No banner")

    end_time = datetime.now()

    print("\nScan completed")
    print("Time taken:", end_time - start_time)
#use 127.0.0.1for testing for output


    
#Combined Vulnerability Scanning

import socket
import requests
import ftplib
from datetime import datetime

# Vulnerability database
vulnerabilities = {
    "Apache/2.2.8": "Old Apache version",
    "OpenSSH_4.7": "Old OpenSSH version",
    "Microsoft-IIS/6.0": "Old IIS version"
}

# 1. Port scanning
def scan_ports(target, ports):
    open_ports = []

    print("\nScanning ports...")

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                print("Open Port:", port)
                open_ports.append(port)

            sock.close()

        except:
            pass

    return open_ports


# 2. Banner grabbing
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))

        banner = sock.recv(1024).decode().strip()
        sock.close()

        return banner

    except:
        return None


# 3. Vulnerability checking
def check_vulnerabilities(banner):
    for version in vulnerabilities:
        if version in banner:
            return vulnerabilities[version]

    return "No known vulnerability"


# 4. FTP login testing (localhost only)
def ftp_bruteforce(target, user, wordlist):
    print("\nFTP Login Testing")

    for password in wordlist:
        try:
            ftp = ftplib.FTP(target, timeout=2)
            ftp.login(user, password)

            print("Login successful:", user, password)
            ftp.quit()
            return

        except:
            print("Login failed:", password)

    print("No valid credentials found")


# 5. SQL injection testing (local test application)
def sql_injection_test(url, param):
    print("\nSQL Injection Testing")

    payloads = ["' OR 1=1 -- ", "' OR 'x'='x"]

    for payload in payloads:
        try:
            new_url = f"{url}?{param}={payload}"
            r = requests.get(new_url, timeout=3)

            if "error" in r.text.lower():
                print("Possible SQL error detected")
            else:
                print("No SQL error detected")

        except:
            print("Request failed")


# 6. Directory checking
def dir_bruteforce(url, wordlist):
    print("\nDirectory Checking")

    for word in wordlist:
        try:
            test_url = f"{url}/{word}"
            r = requests.get(test_url, timeout=3)

            if r.status_code == 200:
                print("Found:", test_url)

        except:
            pass


# MAIN PROGRAM
if __name__ == "__main__":

    target = "127.0.0.1"

    ports = [21, 22, 23, 25, 80, 110, 143, 443, 3389]

    start_time = datetime.now()

    # Port scanning
    open_ports = scan_ports(target, ports)

    # Banner checking
    print("\nBanner Checking")

    for port in open_ports:
        banner = grab_banner(target, port)

        if banner:
            print("Port:", port)
            print("Banner:", banner)
            print("Result:", check_vulnerabilities(banner))
        else:
            print("No banner found")

    # FTP testing - localhost only
    ftp_wordlist = ["1234", "admin", "password", "toor"]
    ftp_bruteforce(target, "admin", ftp_wordlist)

    # SQL testing - local application only
    sql_injection_test("http://127.0.0.1/vulnerable.php", "id")

    # Directory checking - local application only
    wordlist = ["admin", "login", "test", "uploads"]
    dir_bruteforce("http://127.0.0.1", wordlist)

    end_time = datetime.now()

    print("\nScan completed")
    print("Time taken:", end_time - start_time)

