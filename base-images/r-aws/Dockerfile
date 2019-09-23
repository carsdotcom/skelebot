FROM skelebot/r-base
MAINTAINER Sean Shookman <sshookman@cars.com>

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y -q build-essential krb5-user libsasl2-dev libsasl2-modules-gssapi-mit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y r-cran-rjava
RUN apt-get install -y libmariadbclient-dev
RUN apt-get install -y curl
RUN R CMD javareconf
RUN ["Rscript", "-e", "install.packages('RJDBC',repo='https://cloud.r-project.org');library(RJDBC)"]

RUN ["pip3", "install", "pyarrow==0.13.0"]
RUN ["pip3", "install", "s3fs==0.2.1"]
RUN ["pip3", "install", "pandas==0.24.2"]
RUN ["pip3", "install", "pyyaml==5.1.2"]
