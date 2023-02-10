import json
import os
import boto3
import base64
# import sentry_sdk
import requests

# from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# Chatree Cloud Computing Class 8/02/2022

# For CLI program development

# API PATH

PATH_VIEW = os.environ['VIEW_ENDPOINT']
PATH_GET = os.environ['GET_ENDPOINT']
PATH_PUT = os.environ['PUT_ENDPOINT']
PATH_LOGIN = os.environ['LOGIN_ENDPOINT']

def main():
    global username
    print("Welcome to myDropbox Application")
    print("======================================================")
    print("Please put your command.")
    print("""Usage: [options]\n
        Options \n
        view                       view all the file in bucket.
        put <file's name>          put your <file's name> into bucket.
        get <file's name> <email>  get the specific file with your <file's name>
        create <email> <password> <password confirmation>  create your account.
        login <email> <password>    login to your account.
        share <file's name> <email> share your file to your friend.
        quit                        quit the application.
        """)
    print("======================================================")

    while(True):
        command = input(">> ")
        
        #split command intp list of string
        command = command.split(" ")
        if command[0] == "quit":
            username = ""
            print("======================================================")        
            break;
        elif command[0] == "put":
            filename = command[1]
            put(filename)
        elif command[0] == "get":
            filename = command[1]
            fileOwner = command[2] if len(command) == 3 else ""
            get(filename, fileOwner)
        elif command[0] == "view":
            view(username)
        elif command[0] == "login":
            if len(command) != 3:
                print("ERROR: login command is invalid")
                continue
            username = command[1]
            password = command[2]
            login(username, password);
        else:
            print("Command is invalid")

def put(filename):
    global username
    # handle non-exist file
    if not os.path.isfile(filename):
        print("ERROR: File does not exist");
        return

    with open(filename, "rb") as filedata:
        data = filedata.read()
        data = base64.b64encode(data).decode("UTF-8")    

    headers = { "Content-Type": "application/json" }

    # Add directory name (username) before filename 
    filename = username + "/" + filename
    
    raw_body = json.dumps({
        "filename": filename,
        "file": data
    })

    # Send request and Receive response
    response = requests.post(url=PATH_PUT,data=raw_body,headers=headers)

    body = json.loads(response.json()["body"])

    # Catch error
    if(body["result"] == "False"):
        print("ERROR: File does not exist")
        return

    # Check response status
    if response.status_code == 200:
        print("OK")
    else:
        print("ERROR: NOT OK")


def get(filename, fileOwner):
    # Add directory name (username) before filename 
    newfilename = fileOwner + "/" + filename

    headers = { "Content-Type": "application/json" }

    raw_body = json.dumps({
        "filename": newfilename
    })

    # Send request and Receive response
    response = requests.get(url=PATH_GET,data=raw_body,headers=headers)

    body = json.loads(response.json()["body"])

    # Catch error
    if(body["result"] == "False"):
        print("ERROR: File does not exist")
        return

    with open(filename, "wb") as file:
        file.write(base64.b64decode(body["result"]))

    # Handle CLI
    print("OK")
    # Check response status

def view(username):
    
    headers = { "Content-Type": "application/json" }
    raw_body = json.dumps({
        "username": username
    })
    
    # Send request and Receive response
    response = requests.get(url=PATH_VIEW,data=raw_body,headers=headers)

    # Check response status
    if response.status_code == 200:
        body = json.loads(response.json()["body"])

        result = body['result']
        print("OK")
        if(result[0] == ""):
            print("No file in your bucket")
        else:
            for file in result[1:]:
                print(file.strip())
    else:
        print("ERROR: NOT OK")

def login(username, password):
    headers = { "Content-Type": "application/json" }
    raw_body = json.dumps({
        "username": username,
        "password": password
    })

    # Send request and Receive response
    response = requests.post(url=PATH_LOGIN,data=raw_body,headers=headers)

    # Check response status
    if response.status_code == 200:
        print("OK")
    else:
        print("ERROR: NOT OK")

if __name__ == "__main__":
    # Define temporary global variable for collect username and password
    username = ""
    password = ""
    main()

# ++++++ FOR TEST IN LAMBDA TEST ++++++
#  "body": "{\n        \"filename\": \"cp-temp.txt\",\n        \"file\": \"dGVzdA==\"}"
#  "body": "{\n \"username\":\"jhp\",\n \"password\":\"test123\"}"
#  "body": "{\n \"username\":\"jhp\",\n \"filename\":\"test-txt.txt\"}"