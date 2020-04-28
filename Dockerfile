FROM ubuntu:16.04

MAINTAINER Iuliia Zotova  "giulio.rm95@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /githubclient/requirements.txt

WORKDIR /githubclient

RUN pip install Flask
RUN pip install requests
RUN pip install -r requirements.txt

COPY . /githubclient

ENTRYPOINT ["python"]
CMD [ "./run.py" ]