from schema import Schema, And, Optional
from .artifactRepo import ArtifactRepo

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

    def push(self, artifact, version, force=False, user=None, password=None):
        """ Push an artifact to S3 with the given version number """

        pass # TODO

    def pull(self, artifact, version, dest=None, user=None, password=None):
        """ Pull an artifact from S3 with the given version or the LATEST compatible version """

        pass # TODO
