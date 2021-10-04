# Login to Docker Hub with Skelebot user
docker login -u skelebot

# Build and Publish r-base
docker build -t skelebot/r-base base-images/r-base/
docker push skelebot/r-base:latest

# Build and Publish r-krb
docker build -t skelebot/r-krb base-images/r-krb/
docker push skelebot/r-krb:latest

# Build and Publish r-aws
docker build -t skelebot/r-aws base-images/r-aws/
docker push skelebot/r-aws:latest

# Build and Publish r-redshift
docker build -t skelebot/r-redshift base-images/r-redshift/
docker push skelebot/r-redshift:latest

# Build and Publish python-base
docker build -t skelebot/python-base:3.6 -t skelebot/python-base:latest base-images/python-base/3.6/
docker build -t skelebot/python-base:3.7 base-images/python-base/3.7/
docker build -t skelebot/python-base:3.8 base-images/python-base/3.8/
docker build -t skelebot/python-base:3.9 base-images/python-base/3.9/
# Newer Docker clients will push latest by default and will need to do `docker push skelebot/python-base --all-tags`
docker push skelebot/python-base

# Build and Publish python-krb
docker build -t skelebot/python-krb base-images/python-krb/
docker push skelebot/python-krb:latest
