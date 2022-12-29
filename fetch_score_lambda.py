import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime, timedelta

def lambda_handler(event, context):
    s=datetime.utcnow() - timedelta(minutes=5)
    e=datetime.utcnow()
    start=int(s.timestamp())
    end=int(e.timestamp())
    dynamodb = boto3.resource('dynamodb', "us-east-1")
    table = dynamodb.Table('game')
    response = table.scan(
        FilterExpression=Attr('tTime').between(start, end),
    )
    out=[]
    for item in response['Items']:
        out.append({"Items": item['data'],"Total Score": item['total']})
    return {
        'Message': 'Game Detail Fetched',
        'Detail': out
    }
