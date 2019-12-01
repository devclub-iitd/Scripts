from datetime import datetime
from flask import Flask, request, Response
from collections import defaultdict
import requests
import json
from util import *
from mail import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def check():
    return Response("Service Running", status=200)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.data
    request_data = json.loads(data.decode('utf-8'))
    app.logger.error(request_data)
    status = verify_url(request_data['Github Repo URL'])
    if status == 0:
        next_mail(request_data)
    elif status == 1:
        err_mail(request_data, 1)
    else:
        err_mail(request_data, 2)

    return Response("Email Sent", status=200)

if __name__ == '__main__':
    app.run()