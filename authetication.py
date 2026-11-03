users = {'admin': 'password123', 'user1': 'hello123'}

username = input("Enter username: ")
password = input("Enter password: ")

if users.get(username) == password:
    print("Access granted")
else:
    print("Access denied")