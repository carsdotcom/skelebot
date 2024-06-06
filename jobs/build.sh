# Build python-base
docker build -t skelebot/python-base:3.9 -t skelebot/python-base:latest base-images/python-base/3.9/
docker build -t skelebot/python-base:3.10 base-images/python-base/3.10/
docker build -t skelebot/python-base:3.11 base-images/python-base/3.11/

# Build python-krb
docker build -t skelebot/python-krb base-images/python-krb/
