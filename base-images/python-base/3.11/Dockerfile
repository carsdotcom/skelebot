FROM python:3.11-slim
MAINTAINER Sean Shookman <sshookman@cars.com>

# Install basic compilers and libraries commonly needed for downstream packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get upgrade -y && \
    apt-get install -y -q git build-essential libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install -U pip
RUN pip --no-cache-dir install notebook jupyterlab "setuptools>=70.0.0"
