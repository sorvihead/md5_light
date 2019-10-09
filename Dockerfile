FROM python:3.6-alpine

RUN adduser -D tc

WORKDIR /home/tc

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install pymysql

COPY app app
COPY migrations migrations
COPY application.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R tc:tc ./
USER tc

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]