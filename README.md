# **Reko Game**

## **A Game Using Amazon Rekognition**

**Purpose of Solution:**

The purpose of "Reko Game" is to showcase the Amazon Rekognition service. How Amazon Rekognition service is used to identify the objects and the game is designed in such a way that it gives a random score to each object that is detected by Amazon Rekognition Service. It is also a use case of Amplify Service where we have shown one how to configure Amplify to deploy your android Application on the Cloud.

**App Description**

The Reko game is designed using the Amazon Web Services. It is made using Serverless Services like., Amplify, S3, Lambda, Amazon Rekognition, DynamoDB, API Gateway.

In this game the user has to take a picture and upload to S3 Bucket using an Android App. When an object is successfully uploaded to S3 Bucket, AWS Lambda Service has been triggered for identifying the object using Amazon Rekognition Service with the help of boto3 Framework. In the Lambda Function the random value is assigned to each object.

The detailed architecture is shown below:

**Code:**

We have divided the implementation in three stages:

1. Android App to Upload picture to S3 Bucket:
2. Implementation of Lambda Function to identify Object using Amazon Rekognition
3. Fetching DynamoDB Records using API Gateway.
4. HTML code to display Scoreboard

Git Link:

**Implementation:**

This section will cover how to upload a photo from the photo gallery to Amazon S3 using AWS Amplify Storage.

To implement this game, clone the Git project.

Open the project in android studio and configure Amplify service to host android app to cloud environment as shown in the below steps.

**Configuring Amplify**

Start by running the following Amplify CLI terminal command at the root directory of your project:

$ amplify init

Answer the command prompts to finish initializing your Amplify project locally. They should look like this:

? Enter a name for the project uploadtos3android

The following configuration will be applied:

Project information

| Name: uploadtos3android

| Environment: dev

| Default editor: Visual Studio Code

| App type: android

| Res directory: app/src/main/res

? Initialize the project with the above configuration? Yes

Using default provider awscloudformation

? Select the authentication method you want to use: AWS profile

? Please choose the profile you want to use default

Add the Amplify Storage category:

$ amplify add storage

You can select the default answer to most questions by hitting  **Enter**. Here are the answers I selected for the following prompts:

? Select from one of the below mentioned services: Content (Images, audio, video

, etc.)

✔You need to add auth (Amazon Cognito) to your project in order to add storage for user files. Do you want to add auth now? (Y/n) · yes

Using service: Cognito, provided by: awscloudformation

Do you want to use the default authentication and security configuration? Default configuration

How do you want users to be able to sign in? Username

Do you want to configure advanced settings? No, I am done.

✔Provide a friendly name for your resource that will be used to label this category in the project: · s32147b60f

✔Provide bucket name: · uploadtos3android106dd97fb37542bea66e39dfeff2a7

✔Who should have access: · Auth and guest users

✔What kind of access do you want for Authenticated users? · create/update, read, delete

✔What kind of access do you want for Guest users? · create/update, read, delete

✔Do you want to add a Lambda Trigger for your S3 Bucket? (y/N) · yes

Push the Amplify project configuration to the backend.

$ amplify push -y

Once the Storage resources have been successfully created, add the Amplify framework as a dependency for your Android project in the app build.gradle file:

// Amplify

def amplify\_version = "1.31.3"

implementation "com.amplifyframework:aws-storage-s3:$amplify\_version"

implementation "com.amplifyframework:aws-auth-cognito:$amplify\_version"

Now we have to implement a Lambda function which will be triggeredon an image uploaded to S3.

Before creating Lambda Function, we need to Create DynamoDB Table with following fields:

- Table Name: "game"
- Partition key: "tTime" (Timestamp) – [Data Type: Number]

**Lambda Code:**

import json

import urllib.parse

import boto3

import random

from datetime import datetime, timedelta

def lambda\_handler(event, context):

client = boto3.client("rekognition")

s3 = boto3.client("s3")

# reading file from s3 bucket and passing it as bytes

bucket = event['Records'][0]['s3']['bucket']['name']

key = urllib.parse.unquote\_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

fileObj = s3.get\_object(Bucket = bucket, Key=key)

file\_content = fileObj["Body"].read()

# passing bytes data

response = client.detect\_labels(Image = {"Bytes": file\_content}, MinConfidence=70)

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

total= [(a\*data["Dog"]) + (b\*data["Cat"]) + (c\*data["Guitar"]) + (d\*data["Banana"]) + (e\*data["Cricket Ball"])]

tTime=int(datetime.utcnow().timestamp())

# Code to put Score to DynamoDB

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('game')

response = table.put\_item(

Item={'tTime': tTime,'data': data,'total': total}

)

final = {"Data":data,"Total":total}

return json.dumps(final)

Here we stored the score of participants to the DynamoDB table. Now we fetch the last 5 Minutes record using another lambda function which is called by API Gateway to display results to Browser (HTML).

**Lambda to Fetch Record from DynamoDB: Code**

import json

import boto3

from boto3.dynamodb.conditions import Attr, Key

from datetime import datetime, timedelta

def lambda\_handler(event, context):


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

Now we Configure that Lambda to API Gateway:

Step 1: Go to Amazon API Gateway Service and Create API

![](RackMultipart20221229-1-j9dqte_html_35c4d1b83f73a116.png)

Step 2: Create Rest API

![](RackMultipart20221229-1-j9dqte_html_45af6a719420645b.png)

Step 3: Choose Protocols and assign API Name

![](RackMultipart20221229-1-j9dqte_html_e08ba58cf8cfcfc2.png)

Step 4: Create GET API Method

![](RackMultipart20221229-1-j9dqte_html_aa290721b76949b2.png)

Step 5: Configure Lambda Function to that API

![](RackMultipart20221229-1-j9dqte_html_b322c52911470068.png)

Step 6: Deploy API to Stage

![](RackMultipart20221229-1-j9dqte_html_6706a7e2e2b9294e.png)

![](RackMultipart20221229-1-j9dqte_html_42ef67adafbbbf21.png)

Step 7: Copy API Endpoint

![](RackMultipart20221229-1-j9dqte_html_92b4cfe8d42564ec.png)

Configure this API Endpoint to HTML View

**HTML to display Record from API Endpoint: Code**

\<scriptsrc="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"\>\</script\>

\<linkrel="stylesheet"href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"crossorigin="anonymous"\>

\<style\>

    th{

        color:#fff;

            }

    .m{

        color: white;

        font-size: larger;

        font-weight: bolder;

        }

    .center{

        align-items: center;

    }

\</style\>

\<!-- \<h1 style="text-align: center; color: orange;"\> AWS Community Day - Ahmedabad \</h1\> --\>

\<pstyle="text-align: center; padding-top: 10px;"\>\<imgsrc="./download.png"width=35%height=15%class="center"alt="ACDA\_logo"\>\</p\>

\<h2style="text-align: center; color: orange; "\> Game Using Amazon Rekognition \</h2\>

\<tableclass="table table-striped"\>

    \<tr  class="bg-info"\>

        \<th\>Object Detected\</th\>

        \<th\>No. of Object\</th\>

    \</tr\>

    \<tbodyid="myTable"\>

    \</tbody\>

\</table\>

\<script\>

    var myArray = []

    $.ajax({

        method:'GET',

        url:'https://8o779gbd19.execute-api.us-east-1.amazonaws.com/dev',

        headers: {

            'Content-Type': 'application/x-www-form-urlencoded'

        },

        type: "POST", /\* or type:"GET" or type:"PUT" \*/

        dataType: "json",

        data: {

        },

        success:function(response){

            message=response.Message

            myArray = response.Detail

            buildTable(myArray)

            console.log(message)

            console.log(myArray)

        }

    })

    function buildTable(Detail){

        var table = document.getElementById('myTable')

        for (var i = 0; i \< myArray.length; i++){

            var row = `\<tr\>

                            \<td\>${"Banana"}\</td\>

                            \<td\>${myArray[i]["Items"]['Banana']}\</td\>

                      \</tr\>

                      \<tr\>

                            \<td\>${"Cat"}\</td\>

                            \<td\>${myArray[i]["Items"]['Cat']}\</td\>

                      \</tr\>

                      \<tr\>

                            \<td\>${"Cricket Ball"}\</td\>

                            \<td\>${myArray[i]["Items"]['Cricket Ball']}\</td\>

                      \</tr\>

                      \<tr\>

                            \<td\>${"Guitar"}\</td\>

                            \<td\>${myArray[i]["Items"]['Guitar']}\</td\>

                      \</tr\>

                      \<tr\>

                            \<td\>${"Dog"}\</td\>

                            \<td\>${myArray[i]["Items"]['Dog']}\</td\>

                      \</tr\>

                      \<tr class="m bg-info table table-striped"\>

                            \<td\>${"Total Score"}\</td\>

                            \<td\>${myArray[i]["Total Score"]}\</td\>

                      \</tr\>`

            table.innerHTML += row

        }

    }

\</script\>

**DEMO Screenshot:**

**Android App View:**

![](RackMultipart20221229-1-j9dqte_html_4e938768bcddbb7.jpg) ![](RackMultipart20221229-1-j9dqte_html_8c964c81c1f5899e.jpg)

**HTML Score View:**

![](RackMultipart20221229-1-j9dqte_html_adcbf8c2ae3d3c7f.png)

**Conclusion:**

This Article shows how you can build a Game using Amazon Serverless Services like., Amplify, S3, Lambda, Amazon Rekognition, DynamoDB, API Gateway.
