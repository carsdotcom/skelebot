from ...objects.skeleYaml import SkeleYaml

class ArtifactRepo(SkeleYaml):
    """
    Artifact Repo Interface

    Defines the essential functions for an Artifact Repo to implement
    """

    def push(self, artifact, version, force=False, user=None, password=None):
        """ Function to be defined for pushing an artifact to an artifact repository """
        pass

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, password=None):
        """ Function to be defined for pulling an artifact from an artifact repository """
        pass

