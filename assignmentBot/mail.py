from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import *
from util import *


def next_mail(data):
    name = data['Name'].split(' ')[0]
    recipient = data['Email Address']
    topic = data['Assignment']
    link, status = get_next_link(topic, recipient)

    if status == 0:
        return

    content = NEXT_MAIL_TEMPLATE.format(NAME=name, LINK=link, TOPIC=topic)
    send_mail(recipient, content)


def err_mail(data, err_code):
    name = data['Name'].split(' ')[0]
    recipient = data['Email Address']
    topic = data['Assignment']

    if err_code == 1:
        error = "is not a github repo"
    else:
        error = "doesn't exist. Either the repo is private or the link is wrong"

    content = ERR_MAIL_TEMPLATE.format(NAME=name, TOPIC=topic, ERROR=error)
    send_mail(recipient, content)


def send_mail(recipient, content):
    message = MIMEMultipart()
    message['From'] = EMAIL
    message['TO'] = recipient
    message['Subject'] = 'DevClub Winter Assignment'
    message.attach(MIMEText(content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(EMAIL, PASS)

    text = message.as_string()

    session.sendmail(EMAIL, recipient, text)
    session.quit()
