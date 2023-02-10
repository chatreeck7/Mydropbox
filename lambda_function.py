import json
import os
import boto3
import base64
# import sentry_sdk
import requests

# from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# Chatree Cloud Computing Class 8/02/2022

s3 = boto3.client("s3")
# dynamodb = boto3.resource('dynamodb')

# predefine the path name
PATH_VIEW = "/default/acty5-lambda-func/view"
PATH_GET = "/default/acty5-lambda-func/get"
PATH_PUT = "/default/acty5-lambda-func/put"
PATH_LOGIN = "/default/acty5-lambda-func/login"
    
def lambda_handler(event, context):
    
    print(event);
    # receive,define the path and body
    path = event['rawPath']
    body = json.loads(event["body"])
    
    # define bucket's name
    bucket_name = os.environ['BUCKET_NAME']  # < bucket's name
    
    #invoke apiGateWay to get,put from s3
    if path == PATH_VIEW:
        # get all list of files in bucket
        username = body["username"]

        # Call S3 to list all objects in the bucket with the given username
        result = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{username}/")

        # Extract the contents of the response
        contents = result.get("Contents", [])
        file_list = list()
        for content in contents:
            file_name = content["Key"].replace(username+"/", "", 1)
            file_size = content["Size"]
            last_modified = content["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
            file_list.append(f"{file_name} {file_size} {last_modified}")

        return {
            'statuscode': 200,
            'body': json.dumps({"result":file_list})
        }
    elif path == PATH_GET:
        # define the specific filename to get and send it to user
        filename = body["filename"]
        # download the file from S3 to your computer
        try:
            # Download the file
            obj = s3.get_object(Bucket=bucket_name, Key=filename)
            file = obj["Body"].read()
            encoded_string = base64.b64encode(file).decode("utf-8")
            
        except Exception as e:
            print(f"Something went wrong: {e}")
            return {
                'statuscode': 999,
                'body': json.dumps({'result':"False"})
            }
        return {
            'statuscode': 200,
            'body': json.dumps({'result':encoded_string})
        }
        
    elif path == PATH_PUT:
        # define the specific filename to put it to s3
        filename = body["filename"]         # < fime's name
        filedata = body["file"]             # < file data
        s3.put_object(Bucket=bucket_name, Key=filename,Body=base64.b64decode(filedata))
        return {
            'statuscode': 200,
            'body': json.dumps({'result': 'True'})
        }
    elif path == PATH_LOGIN:
        password = body["password"]
        username = body["username"]
        folder_name = username+"/"
        # create the folder
        
        try:
            # Download the file
            s3.put_object(Bucket=bucket_name, Key=folder_name)
            
        except Exception as e:
            print(f"Something went wrong: {e}")
            return {
                'statuscode': 999,
                'body': json.dumps({'result':"False"})
            }
        
        return {
            'statuscode': 200,
            'body': json.dumps({'result':'True'})
        }