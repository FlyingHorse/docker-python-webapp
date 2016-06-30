FROM ubuntu:14.04
MAINTAINER yangyang.liu@stupa
RUN apt-get update
RUN apt-get install -y -q python-all python-pip wget
RUN wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python_2.1.3-1ubuntu14.04_all.deb
RUN dpkg -i mysql-connector-python_2.1.3-1ubuntu14.04_all.deb 
RUN apt-get -yq install curl
RUN pip install jinja2
ADD ./www /opt/webapp
WORKDIR /opt/webapp
EXPOSE 9000
CMD ["python", "wsgiapp.py"]
