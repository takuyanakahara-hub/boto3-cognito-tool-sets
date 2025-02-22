import boto3, hmac, base64, hashlib

class CustomCognitoIdp:
    """ CognitoをPythonから呼び出せるライブラリ

    想定の利用:
        ・ローカルからローカルのCognito操作
        ・ローカルからクラウド上のCognito操作
        ・クラウドからクラウドへのCognito操作

    """
    def __init__(
        self, 
        PROFILE_NAME,
        COGNITO_ENDPOINT,
        REGION,
        USERPOOL_ID,
        CLIENT_ID,
        SECRET,
    ):
        self.PROFILE_NAME = PROFILE_NAME
        self.COGNITO_ENDPOINT = COGNITO_ENDPOINT
        self.REGION = REGION
        self.USERPOOL_ID = USERPOOL_ID
        self.CLIENT_ID = CLIENT_ID
        self.SECRET = SECRET
    
    def set_client(self):
        if self.PROFILE_NAME != "":
            session = boto3.Session(profile_name=self.PROFILE_NAME)
        else:
            session = boto3.Session()
        config = boto3.session.Config(proxies={})
        client = session.client(
            "cognito-idp",
            endpoint_url = self.COGNITO_ENDPOINT,
            region_name = self.REGION,
            config = config,
        )
        return client
    
    def create_secret_hash(self, username):
        message, key = (username + self.CLIENT_ID).encode("utf-8"), self.SECRET.encode("utf-8")
        hmac_secret = hmac.new(key, message, digestmod=hashlib.sha256)
        secret_hash = base64.b64encode(hmac_secret.digest())
        return secret_hash
    
    def get_userpools(self, client, num):
        try:
            response = client.list_user_pools(
                MaxResults=num,
            )
        except Exception as e:
            print("error message: ", e)
        userpools = response.get("UserPools")
        return userpools
    
    def describe_user_pool(self, client):
        try:
            response = client.describe_user_pool_client(
                UserPoolId = self.USERPOOL_ID,
            )
        except Exception as e:
            print("error message: ", e)
        
        return response
    
    def create_userpools(self, client, userpool_name):
        try:
            response = client.create_user_pool(
                PoolName=userpool_name,
            )
        except Exception as e:
            print("error message: ", e)
        userpool = response.get("UserPool")
        return userpool
    
    def get_userpool_clients(self, client):
        try:
            response = client.list_user_pool_clients(
                UserPoolId=self.USERPOOL_ID,
            )
        except Exception as e:
            print("error message: ", e)
        userpool_clients = response.get("UserPoolClients")
        return userpool_clients
    
    def describe_userpool_client(self, client):
        try:
            response = client.describe_user_pool_client(
                UserPoolId=self.USERPOOL_ID,
                ClientId=self.CLIENT_ID,
            )
        except Exception as e:
            print("error message: ", e)
        userpool_client = response.get("UserPoolClient")
        return userpool_client
    
    def create_app_client(self, client, client_name):
        try:
            response = client.create_user_pool_client(
                UserPoolId=self.USERPOOL_ID,
                ClientName=client_name,
                GenerateSecret=True,
            )
        except Exception as e:
            print("error message: ", e)
        return response
    
    def get_list_users(self, client):
        try:
            response = client.list_users(
                UserPoolId=self.USERPOOL_ID,
            )
        except Exception as e:
            print("error message: ", e)
        users = response.get("Users")
        return users
    
    def create_user(self, client, username, password, email=None):
        try:
            client.admin_create_user(
                UserPoolId=self.USERPOOL_ID,
                Username=username,
                UserAttributes=[
                    {
                        "Name": "email",
                        "Value": email,
                    }
                ]
            )
            client.admin_set_user_password(
                UserPoolId=self.USERPOOL_ID,
                Username=username,
                Password=password,
                Permanent=True
            )
        except Exception as e:
            print("error message: ", e)
        return {
            "message": "Success create new user!"
        }
    
    def login(self, client, username, password, secret):
        try:
            response = client.initiate_auth(
                ClientId=self.CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": secret,
                }
            )
        except Exception as e:
            print("error message: ", e)
        
        tokens = response.get("AuthenticationResult")
        return {
            "Tokens": tokens,
        }
    
    