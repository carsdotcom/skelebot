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

# Build and Publish python-base
docker build -t skelebot/python-base base-images/python-base/
docker push skelebot/python-base:latest

# Build and Publish python-krb
docker build -t skelebot/python-krb base-images/python-krb/
docker push skelebot/python-krb:latest
