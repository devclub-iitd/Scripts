from datetime import datetime
from flask import Flask, request
from collections import defaultdict
import requests
from util import *
from mail import *

users = defaultdict(int)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def check():
    return "Service Running"

@app.route("/submit", methods=["POST"])
def submit():
    request_data = request.get_json()
    if verify_url(request_data['Github Repo URL']):
        next_mail(request_data)
    else:
        err_mail(request_data)

if __name__ == '__main__':
    app.run()