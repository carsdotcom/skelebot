import os
import yaml
import boto3
import argparse
import pandas as pd
import pyarrow.parquet as pq

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

    def connect(self):
        """ Establish connection to S3 with region and profile and return the client"""
        session = boto3.Session(profile_name=self.profile, region_name=self.region)
        client = session.client('s3')
        return client

    def push(self, artifact, version, force=False, user=None, password=None):
        """ Push an artifact to S3 with the given version number """

        client = connect()

        artifactName = artifact.getVersionedName(version)
        client.upload_file(artifact.file, self.bucket, artifactName)

        # TODO: Handle Exceptions
        # TODO: Need to allow for pushing of artifact with version number
        # TODO: Need to prevent pushing if the artifact already exists
        # TODO: Need to allow for forcing a push if the flag is set

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, password=None):
        """ Pull an artifact from S3 with the given version or the LATEST compatible version """

        # TODO: Handle Exceptions

        client = connect()

        #if (version == "LATEST"):
            # TODO: Identify latest compatible version of the artifact in the bucket

        artifactName = artifact.getVersionedName(version)
        dest = artifact.file if (override) else artifactName
        client.download_file(self.bucket, artifactName, dest)
