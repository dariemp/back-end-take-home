FROM tiangolo/uwsgi-nginx-flask:python3.7

ADD requirements.txt .
RUN pip install -r requirements.txt
COPY ./src /app
