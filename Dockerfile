FROM python:3.9.2
WORKDIR /code
COPY ./foodgram .
COPY ./requirements.txt .
RUN pip install -r /code/requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
