FROM r-base:3.6.3
MAINTAINER Sean Shookman <sshookman@cars.com>

RUN apt-get update
RUN apt-get install -y jupyter

RUN ["Rscript", "-e", "install.packages('IRkernel', repo='https://cloud.r-project.org'); IRkernel::installspec()"]

RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libssl-dev
RUN apt-get install -y libxml2-dev
RUN apt-get install -y gfortran
RUN ["Rscript", "-e", "install.packages('glue', repo='https://cloud.r-project.org'); library(glue)"]
RUN ["Rscript", "-e", "install.packages('devtools', repo='https://cloud.r-project.org'); library(devtools)"]
RUN apt-get install -y python3-pip
RUN pip --no-cache-dir install jupyterlab
