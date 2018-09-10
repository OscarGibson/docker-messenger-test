FROM python:3.6.1 as builder

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install wkhtmltopdf tool
#RUN apt-get update
#RUN apt-get install pandoc
#RUN apt-get install xvfb libfontconfig libcairo2-dev libjpeg62-turbo-dev libpango1.0-dev libgif-dev build-essential g++ xfonts-75dpi -y
#RUN wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb
#RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.1/wkhtmltox-0.12.1_linux-wheezy-amd64.deb
#RUN dpkg -i wkhtmltox-0.12.1_linux-wheezy-amd64.deb
#RUN sudo mv wkhtmltox_0.12.5-1.xenial_amd64.deb /usr/local/bin/wkhtmltopdf
#RUN sudo chmod +x /usr/local/bin/wkhtmltopdf


# add requirements (to leverage Docker cache)
ADD ./requirements/development.txt /usr/src/app/requirements/development.txt

# install requirements
RUN pip install -r requirements/development.txt

# create database
CMD python manage.py recreate_db

# seed db
CMD python manage.py seed_db

# run server
CMD python manage.py runserver -h 0.0.0.0