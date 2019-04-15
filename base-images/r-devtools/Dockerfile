FROM skelebot/r-base
MAINTAINER Sean Shookman <sshookman@cars.com>

RUN apt-get update
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libssl-dev
RUN apt-get install -y libxml2-dev
RUN ["Rscript", "-e", "install.packages('devtools', repo='https://cloud.r-project.org'); library(devtools)"]
