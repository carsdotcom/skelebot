FROM r-base:3.5.0
MAINTAINER Sean Shookman <sshookman@cars.com>

RUN apt-get update
RUN apt-get install -y jupyter
RUN ["Rscript", "-e", "install.packages('IRkernel', repo='https://cloud.r-project.org'); IRkernel::installspec()"]
