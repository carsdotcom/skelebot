# Build r-base
docker build -t skelebot/r-base base-images/r-base/

# Build r-krb
docker build -t skelebot/r-krb base-images/r-krb/

# Build r-aws
docker build -t skelebot/r-aws base-images/r-aws/

# Build r-redshift
docker build -t skelebot/r-redshift base-images/r-redshift/

# Build python-base
docker build -t skelebot/python-base:3.6 -t skelebot/python-base:latest base-images/python-base/3.6/
docker build -t skelebot/python-base:3.7 base-images/python-base/3.7/
docker build -t skelebot/python-base:3.8 base-images/python-base/3.8/
docker build -t skelebot/python-base:3.9 base-images/python-base/3.9/
docker build -t skelebot/python-base:3.10 base-images/python-base/3.10/
docker build -t skelebot/python-base:3.11 base-images/python-base/3.11/

# Build python-krb
docker build -t skelebot/python-krb base-images/python-krb/
