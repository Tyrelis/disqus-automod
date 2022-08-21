## Introduction
A web-based application written in Python, utilising Flask web framework and Disqus API to ease the moderation and logging for Disqus Moderation.

## Requirements
* flask >= 1.1.2
* flask-mysqldb >= 0.2.0
* discord-webhook >= 0.11.0
* yaml >= 0.2.5


## Configuration

Make a file called ```db.yaml``` in the same directory as ```app.py```which contains the following content.

```
#API Access
API_KEY: ENTER YOUR DISQUS API KEY HERE
access_token: ENTER YOUR DISQUS ACCESS TOKEN HERE

#DATABASE
HOST: HOST OF YOUR DATABASE
USER: USER ACCOUNT OF YOUR DATABASE
PASSWORD: PASSWORD FOR THE USER ACCOUNT
DB: NAME OF THE DATABASE

#DISCORD
WEBHOOK: WEBHOOK URL TO THE CHANNEL WHICH YOU WANT TO USE AS THE LOGGING CHANNEL
```


## Installation

Once you've make configured ```db.yaml```, run the following command in the terminal in the root directory.

```flask run```
