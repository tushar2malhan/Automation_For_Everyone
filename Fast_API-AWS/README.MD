### Simple Serverless FastAPI with AWS Lambda Complete Walkthrough
    
    []: # Language: Python
    []: # Path: app\README.MD

## Points to be noted 
- flask vs fastapi == no data validation in flask but with enum in fastapi
- FastApi much Faster than Flask


## Installation

### Setup Virtual Environment

```Windows 
pip install virtualenv
pip -m virtualenv name_of_virtualenv
.\env\Scripts\activate
```
```Linux 
virtualenv -p python3.7 env
source ./env/bin/activate
```

### Install Dependencies

```shell
pip install -r requirements.txt
```

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
The server would be running on http://localhost:8080



## Deploy

### Package Dependencies

- Activate The Virtual Environment
* pip install mangum    (Handler for Lambda functions)
- In the Root app Use Mangum(app)

```
cd env/Lib/site-packages/
zip -r ../../../../funtion.zip .
```
* You can check this function zip file would be available in your Directory where all your dependencies will be stored

* For ubuntu systems
```shell
cd env/lib/python3.7/site-packages
zip -r9 /path/to/root/function.zip
```
 
* Now you will need to put your App(Which consits of FastAPI) directory in ur function.zip | We Package Lambda 
```
zip -g ../function.zip -r app/
```



* Now Once You login to AWS via IAM you will be able to create a new function and S3 bucket
- Create a new S3 bucket
- Upload the function.zip to S3
- Create a new LAMBDA function
* Api gateway and lambda should be in same region 
- Under Actions - Upload the function.zip from S3 bucket to Lambda function
- In Basic settings of the Lambda function you can set the handler to be app.main.handler
- In the Advanced settings of the Lambda function you can set the runtime to be python3.7
- Test the Lambda function where event Template is apigateway-aws-proxy and set the event name to be "test"
- set the path: '/' and method: 'GET' in json file
* SUCCESS MESSAGE


## API Gateway 
- Rest API Gateway is a web service that allows you to expose APIs in a simple, declarative way.
- Use it and create an API
- Under Actions - Create Method , set path to ANY and mark the checklist and for the integration use lambda function which was created in previous step
- Click on ANY and create a resource where everything will be default and save it .
- Under API Actions - click Deploy API  and set the stage by just giving a name
- FINALLY YOU CAN TEST THE API with the url shown

## For any issue 
- Check Screenshot Directory 
