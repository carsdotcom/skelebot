# The preferred way to publish to Docker Hub is now via .github/workflows/publish-base-images.yaml
# We keep this script in case there is a need for a manual push

# Note: To get multi-platform builds working see:
# https://docs.docker.com/build/building/multi-platform/
# https://docs.docker.com/desktop/features/containerd/

# Login to Docker Hub with Skelebot user
docker login -u skelebot

# Build and Publish python-base
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.9 -t skelebot/python-base:latest base-images/python-base/3.9/
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.10 base-images/python-base/3.10/
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.11 base-images/python-base/3.11/
# Newer Docker clients will push latest by default and will need to do `docker push skelebot/python-base --all-tags`
docker push skelebot/python-base --all-tags

# Build and Publish python-krb
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-krb base-images/python-krb/
docker push skelebot/python-krb:latest
