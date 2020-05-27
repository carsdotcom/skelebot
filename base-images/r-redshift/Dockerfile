FROM skelebot/r-base
MAINTAINER Joao Moreira <jmoreira@cars.com>

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends openjdk-8-jdk git curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the Redshift driver
RUN R CMD javareconf
RUN ["Rscript", "-e", "install.packages('RJDBC',repo='https://cloud.r-project.org');library(RJDBC)"]
RUN mkdir -p /usr/lib/redshift/lib && \
    cd /usr/lib/redshift/lib && \
    curl -O http://s3.amazonaws.com/redshift-downloads/drivers/RedshiftJDBC41-1.1.9.1009.jar

# Install the AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip
