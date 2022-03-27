from flask import Flask
from os import getenv

app=Flask(__name__)
app.secret_key='abe21dfacacf1c28599759147352b486'#getenv('SECRET_KEY')#what is this used for?

import routes