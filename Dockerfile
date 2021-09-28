FROM ubuntu:18.04

RUN apt-get update

ENV HOME /root

WORKDIR /root

RUN apt-get update --fix-missing
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install bottle
RUN pip3 install firebase
RUN pip3 install setuptools_rust
RUN pip3 install python_jwt
RUN pip3 install gcloud
RUN pip3 install sseclient
RUN pip3 install pycryptodome
RUN pip3 install requests_toolbelt
RUN apt-get install -y nodejs
RUN apt-get install -y npm


COPY . .

#Run main.py
CMD python3 main.py $PORT


EXPOSE $PORT


