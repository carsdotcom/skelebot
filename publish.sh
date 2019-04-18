# Get Version from skelebot.yaml
version=$(cat skelebot/globals.py | grep IMAGE_VERSION | awk '{ print $NF }')

# Login to Docker Hub with Skelebot user
docker login -u skelebot

# Build and Publish r-base
docker build -t skelebot/r-base base-images/r-base/
docker tag skelebot/r-base:latest skelebot/r-base:$version
docker push skelebot/r-base:latest
docker push skelebot/r-base:$version

# Build and Publish r-devtools
docker build -t skelebot/r-devtools base-images/r-devtools/
docker tag skelebot/r-devtools:latest skelebot/r-devtools:$version
docker push skelebot/r-devtools:latest
docker push skelebot/r-devtools:$version

# Build and Publish r-krb
docker build -t skelebot/r-krb base-images/r-krb/
docker tag skelebot/r-krb:latest skelebot/r-krb:$version
docker push skelebot/r-krb:latest
docker push skelebot/r-krb:$version

# Build and Publish python-base
docker build -t skelebot/python-base base-images/python-base/
docker tag skelebot/python-base:latest skelebot/python-base:$version
docker push skelebot/python-base:latest
docker push skelebot/python-base:$version

# Build and Publish python-krb
docker build -t skelebot/python-krb base-images/python-krb/
docker tag skelebot/python-krb:latest skelebot/python-krb:$version
docker push skelebot/python-krb:latest
docker push skelebot/python-krb:$version
