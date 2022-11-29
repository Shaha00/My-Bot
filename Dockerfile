FROM python:3.10

EXPOSE 2007

RUN mkdir -p /opt/services/bot
WORKDIR /opt/services/bot

COPY . /opt/services/bot

RUN pip install -r requirements.txt

CMD ["python", "/opt/services/bot/main.py"]