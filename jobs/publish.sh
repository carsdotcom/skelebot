# Login to Docker Hub with Skelebot user
docker login -u skelebot

# Build and Publish python-base
docker build -t skelebot/python-base:3.9 -t skelebot/python-base:latest base-images/python-base/3.9/
docker build -t skelebot/python-base:3.10 base-images/python-base/3.10/
docker build -t skelebot/python-base:3.11 base-images/python-base/3.11/
# Newer Docker clients will push latest by default and will need to do `docker push skelebot/python-base --all-tags`
docker push skelebot/python-base --all-tags

# Build and Publish python-krb
docker build -t skelebot/python-krb base-images/python-krb/
docker push skelebot/python-krb:latest
