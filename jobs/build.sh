# Note: To get multi-platform builds working see:
# https://docs.docker.com/build/building/multi-platform/
# https://docs.docker.com/desktop/features/containerd/

# Build python-base
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.9 -t skelebot/python-base:latest base-images/python-base/3.9/
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.10 base-images/python-base/3.10/
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-base:3.11 base-images/python-base/3.11/

# Build python-krb
docker build --platform=linux/amd64,linux/arm64 -t skelebot/python-krb base-images/python-krb/
