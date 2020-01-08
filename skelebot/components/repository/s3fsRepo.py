import boto3
from schema import Schema, And, Optional
from .artifactRepo import ArtifactRepo
from ...objects.semver import Semver

class S3fsRepo(ArtifactRepo):
    """
    S3 File System Class

    S3 connection details for saving artifacts in AWS S3 buckets
    """

    schema = Schema({
        'bucket': And(str, error='S3fs \'bucket\' must be a String'),
        'region': And(str, error='S3fs \'region\' must be a String'),
        Optional('profile'): And(str, error='S3fs \'profile\' must be a String'),
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

        client = self.connect()

        artifactName = artifact.getVersionedName(version)
        client.upload_file(artifact.file, self.bucket, artifactName)

        # TODO: Handle Exceptions
        # TODO: Need to allow for pushing of artifact with version number
        # TODO: Need to prevent pushing if the artifact already exists
        # TODO: Need to allow for forcing a push if the flag is set

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, password=None):
        """ Pull an artifact from S3 with the given version or the LATEST compatible version """

        client = self.connect()

        # Identify the latest compatible version
        if (version == "LATEST"):
            version = None
            currentSemver = Semver(currentVersion)
            ext = artifact.file.split(".")[1]
            response = client.list_objects(Bucket=self.bucket, Prefix=artifact.name)

            # Iterate through all the artifacts int he bucket
            for content in response["Contents"]:
                artifactSemver = Semver(str(content["Key"]).split("_v")[1].split(ext)[0])

                # Find the most recent backward compatible version AKA Latest Compatible Version (LCV)
                if (currentSemver.isBackwardCompatible(artifactSemver)) and ((version is None) or (version < artifactSemver)):
                    version = artifactSemver

            if (version is None):
                raise RuntimeError(self.ERROR_NOT_COMPATIBLE)

        artifactName = artifact.getVersionedName(version)
        dest = artifact.file if (override) else artifactName

        try:
            client.download_file(self.bucket, artifactName, dest)
        except:
            raise RuntimeError("Failed to Locate the Specified Artifact")
