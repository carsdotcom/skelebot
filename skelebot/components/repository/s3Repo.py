import boto3
from schema import Schema, And, Optional
from .artifactRepo import ArtifactRepo
from ...objects.semver import Semver

class S3Repo(ArtifactRepo):
    """
    S3 File System Class

    S3 connection details for saving artifacts in AWS S3 buckets
    """

    schema = Schema({
        'bucket': And(str, error="S3 'bucket' must be a String"),
        'region': And(str, error="S3 'region' must be a String"),
        Optional('profile'): And(str, error="S3 'profile' must be a String"),
    }, ignore_extra_keys=True)

    bucket = None
    region = None
    profile = None

    def __init__(self, bucket, region, profile):
        """ Initialize the needed values for any S3 connection """
        self.bucket = bucket
        self.region = region
        self.profile = profile

    def connect(self):
        """ Establish connection to S3 with region and profile and return the client"""
        session = boto3.Session(profile_name=self.profile, region_name=self.region)
        client = session.client('s3')
        return client

    def push(self, artifact, version, force=False, user=None, password=None):
        """ Push an artifact to S3 with the given version number """

        bucket_parts = self.bucket.split("/")
        bucket_parts.append(artifact.getVersionedName(version))
        bucket = bucket_parts[0]
        path = "/".join(bucket_parts[1:])

        # If the object exists and we are not force pushing, raise an error
        client = self.connect()
        if (not force):
            response = client.list_objects_v2(Bucket=bucket, Prefix=path)
            if ("Contents" in response.keys()):
                print(response["Contents"][0]["Key"])
                raise RuntimeError(self.ERROR_ALREADY_PUSHED)

        # Upload the artifact with the versioned name
        client.upload_file(artifact.file, bucket, path)

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, password=None):
        """ Pull an artifact from S3 with the given version or the LATEST compatible version """

        # Identify the latest compatible version
        client = self.connect()
        if (version == "LATEST") and (artifact.singular == False):
            version = None
            currentSemver = Semver(currentVersion)
            ext = artifact.file.split(".")[1]
            prefix = "{name}_v{major}".format(name=artifact.name, major=currentSemver.major)

            bucket_parts = self.bucket.split("/")
            bucket = bucket_parts[0]
            bucket_parts.append(prefix)
            path = "/".join(bucket_parts[1:])
            response = client.list_objects_v2(Bucket=bucket, Prefix=path)

            # Iterate through all the artifacts int he bucket
            for content in response["Contents"]:
                artifactSemver = Semver(str(content["Key"]).split("_v")[1].split(ext)[0])

                # Find the most recent backward compatible version AKA Latest Compatible Version (LCV)
                if (currentSemver.isBackwardCompatible(artifactSemver)) and ((version is None) or (version < artifactSemver)):
                    version = artifactSemver

            # Raise an error if no LCV is found
            if (version is None):
                raise RuntimeError(self.ERROR_NOT_COMPATIBLE)

        # Download the artifact based on the version provided or LCV
        artifactName = artifact.getVersionedName(version)
        dest = artifact.file if (override) else artifactName

        bucket_parts = self.bucket.split("/")
        bucket = bucket_parts[0]
        bucket_parts.append(artifactName)
        path = "/".join(bucket_parts[1:])

        client.download_file(bucket, path, dest)
