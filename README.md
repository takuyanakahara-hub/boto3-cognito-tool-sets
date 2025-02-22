# boto3-cognito-tools-sets
This is a toolset summarizing the key features of the boto3 library for operating Amazon Cognito with Python.

It is a simpler yet powerful tool that can be useful for testing and development.
By switching script variables, it maintains compatibility between local and cloud environments.

However, please note that the configuration is not universally applicable in all cases.

# Get Start

```
$ pwd
> ~~/boto3-cognito-tools-sets

$ git clone <this repository>
```

# local cognito setup
Active pyenv, virtualenv for use python enviroments 3.12.xx

```
$ pip install boto3, moto[server]
$ moto_server -p3000
```

## initial local cognito create
Please perform this operation only once at the initial startup.

```python
from cognito_idp import CustomCognitoIdp

PROFILE_NAME = ""
COGNITO_ENDPOINT = "http://127.0.0.1:3000"
REGION = "ap-northeast-1"
USERPOOL_ID = ""
CLIENT_ID = ""
SECRET = ""

idp = CustomCognitoIdp(
    PROFILE_NAME = PROFILE_NAME,
    COGNITO_ENDPOINT = COGNITO_ENDPOINT,
    REGION = REGION,
    USERPOOL_ID = USERPOOL_ID,
    CLIENT_ID = CLIENT_ID,
    SECRET = SECRET,
)

client = idp.set_client()
idp.create_userpools(client=client, userpool_name="sample")
userpools = idp.get_userpools(client=client, num=10)

USERPOOL_ID = userpools[0].get("Id")
idp = CustomCognitoIdp(
    PROFILE_NAME = PROFILE_NAME,
    COGNITO_ENDPOINT = COGNITO_ENDPOINT,
    REGION = REGION,
    USERPOOL_ID = USERPOOL_ID,
    CLIENT_ID = CLIENT_ID,
    SECRET = SECRET,
)
idp.create_app_client(client=client, client_name="sample-client-2")

app_clients = idp.get_userpool_clients(client=client)
client_id = app_clients[0].get("ClientId")
CLIENT_ID = client_id
idp = CustomCognitoIdp(
    PROFILE_NAME = PROFILE_NAME,
    COGNITO_ENDPOINT = COGNITO_ENDPOINT,
    REGION = REGION,
    USERPOOL_ID = USERPOOL_ID,
    CLIENT_ID = CLIENT_ID,
    SECRET = SECRET,
)

app_client = idp.describe_userpool_client(client=client)

SECRET = app_client.get("ClientSecret")

idp = CustomCognitoIdp(
    PROFILE_NAME = PROFILE_NAME,
    COGNITO_ENDPOINT = COGNITO_ENDPOINT,
    REGION = REGION,
    USERPOOL_ID = USERPOOL_ID,
    CLIENT_ID = CLIENT_ID,
    SECRET = SECRET,
)

idp.create_user(client=client, username="admin@admin.co.jp", password="@Password0", email="admin@admin.co.jp")
```

When use email & password, you completed login and You'll get OIDC tokens!