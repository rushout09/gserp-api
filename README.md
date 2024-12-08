
# GSERP API

## Overview

The GSERP API is an open-source project designed to perform search queries on Google and return organic search results. It leverages the `requests-ip-rotator` to handle IP rotation, ensuring that requests are made from different IP addresses to avoid being blocked by Google. The API is built using Python and provides a simple interface for querying and retrieving search results.

## Features

- **IP Rotation**: Utilizes `requests-ip-rotator` to rotate IP addresses for each request.
- **Customizable Search**: Allows specifying search parameters such as country, language, location, and fields to retrieve.
- **Field Selection**: Users can choose which fields to include in the search results, such as title, link, snippet, etc.
- **Error Handling**: Provides detailed error messages for invalid field selections and connection issues.

## Installation

```
pip install gserp-api
```

or from source:

```
git clone git@github.com:rushout09/gserp-api.git
cd gserp-api
python3 -m venv venv
source venv/bin/activate
pip install -r requriements.txt
```

## Usage

```
import os
from requests_ip_rotator import ApiGateway
from gserp_api import search

# Set AWS credentials
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Create and start an API Gateway
gateway = ApiGateway("https://www.google.com", access_key_id=aws_access_key_id, secret_access_key=aws_secret_access_key)
gateway.start()

try:
    # Perform a search
    query = "OpenAI GPT-4"
    fields = ["title", "link", "snippet"]
    results = search(gateway, query, *fields, country="US", lang="en")
    print(results)

finally:
    # Shut down the API Gateway
    gateway.shutdown()
```

## How to get AWS Credentials

To obtain AWS credentials, you need to create an IAM user in the AWS Management Console and assign the necessary permissions. Here’s a step-by-step guide:

How to Get AWS Credentials

1. Sign in to AWS Management Console:
Go to the AWS Management Console.
Sign in with your AWS account credentials.

2. Navigate to IAM (Identity and Access Management):
In the AWS Management Console, search for "IAM" in the services search bar and select it.

3. Create a New IAM User:
In the IAM dashboard, click on "Users" in the left sidebar.
Click the "Add user" button.
Enter a username for the new user.
Select the "Programmatic access" checkbox to generate an access key ID and secret access key.

4. Set Permissions:
Choose how you want to set permissions for the user. You can either:
Attach existing policies directly (e.g., AmazonS3FullAccess for S3 access).
Add the user to a group with the necessary permissions.
Copy permissions from an existing user.
Attach custom policies if needed.

5. Review and Create User:
Review the user details and permissions.
Click "Create user".

6. Download Credentials:
After the user is created, you will see the access key ID and secret access key.
Download the .csv file containing these credentials or copy them to a secure location. You will not be able to view the secret access key again.

7. Set Environment Variables:
On your local machine, set the AWS credentials as environment variables:
your_secret_access_key

8. Use Credentials in Your Application:
Your application can now use these environment variables to authenticate with AWS services.