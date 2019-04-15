docker login -u skelebot

docker build -t skelebot/r-base base-images/r-base/
docker push skelebot/r-base

docker build -t skelebot/r-devtools base-images/r-devtools/
docker push skelebot/r-devtools

docker build -t skelebot/r-krb base-images/r-krb/
docker push skelebot/r-krb

docker build -t skelebot/python-base base-images/python-base/
docker push skelebot/python-base

docker build -t skelebot/python-krb base-images/python-krb/
docker push skelebot/python-krb
