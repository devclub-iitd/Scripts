FROM python:3.6-alpine

RUN mkdir /bot
WORKDIR /bot

COPY assignmentBot/requirements.txt /bot/
RUN pip install -Ur requirements.txt

COPY assignmentBot/* /bot/

CMD ["flask", "run", "--host=0.0.0.0"]