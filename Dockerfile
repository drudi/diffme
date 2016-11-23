FROM python:3.5

ADD api /app/api
ADD tests /app/tests
ADD app.py /app/
ADD run_api.sh /app/
ADD requirements.txt /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ./run_api.sh
