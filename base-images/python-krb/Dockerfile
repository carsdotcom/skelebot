FROM skelebot/python-base
MAINTAINER Sean Shookman <sshookman@cars.com>

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y -q krb5-user libsasl2-dev libsasl2-modules-gssapi-mit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY init.sh /krb/
RUN chmod +x /krb/init.sh
