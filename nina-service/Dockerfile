FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements/development.txt /usr/src/app/requirements/development.txt

# install requirements
RUN pip install -r requirements/development.txt

# create database
CMD python manage.py recreate_db

# run server
CMD python manage.py runserver -h 0.0.0.0
