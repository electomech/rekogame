import json
import urllib.parse
import boto3
import random
from datetime import datetime, timedelta

def lambda_handler(event, context):
    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    # reading file from s3 bucket and passing it as bytes
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    fileObj = s3.get_object(Bucket = bucket, Key=key)
    file_content = fileObj["Body"].read()
    # passing bytes data
    response = client.detect_labels(Image = {"Bytes": file_content}, MinConfidence=70)

    data={"Dog":0,"Cat":0,"Guitar":0,"Banana":0,"Cricket Ball":0}
    for obj1 in response["Labels"]:
        if obj1["Name"]=="Dog":
            data.update({"Dog":(len(obj1["Instances"]))})
    for obj2 in response["Labels"]:
        if obj2["Name"]=="Cat":
            data.update({"Cat":(len(obj2["Instances"]))})
    for obj3 in response["Labels"]:
        if obj3["Name"]=="Guitar":
            data.update({"Guitar":(len(obj3["Instances"]))})
    for obj4 in response["Labels"]:
        if obj4["Name"]=="Banana":
            data.update({"Banana":(len(obj4["Instances"]))})
    for obj5 in response["Labels"]:
        if obj5["Name"]=="Cricket Ball":
            data.update({"Cricket Ball":(len(obj5["Instances"]))})
    a=random.randint(1,10)
    b=random.randint(1,10)
    c=random.randint(1,10)
    d=random.randint(1,10)
    e=random.randint(1,10)

    total= [(a*data["Dog"]) + (b*data["Cat"]) + (c*data["Guitar"]) + (d*data["Banana"]) + (e*data["Cricket Ball"])]
    tTime=int(datetime.utcnow().timestamp())

# Code to put Score to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('game')
    response = table.put_item(
        Item={'tTime': tTime,'data': data,'total': total}
    )
    final = {"Data":data,"Total":total}
    return json.dumps(final)
