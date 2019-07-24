# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten during Skelebot execution
FROM skelebot/python-base
MAINTAINER Sean Shookman <sshookman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
COPY . /app
CMD /bin/bash -c './/app/test.sh'
