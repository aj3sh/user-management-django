# Base Image
FROM python:3.8-slim-buster

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory app to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000

# Install project dependencies
RUN pip install -r requirements.txt --default-timeout=1000
RUN pip install gunicorn

EXPOSE $PORT
# CMD python manage.py runserver 0.0.0.0:$PORT