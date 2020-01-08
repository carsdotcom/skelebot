from unittest import TestCase, main
import skelebot as sb

class TestArtifactRepo(TestCase):

    def test_push_pass(self):
        artifactRepo = sb.components.repository.artifactRepo.ArtifactRepo()
        nothing = artifactRepo.push("artifact", "1.1.0", force=False, user=None, password=None)
        self.assertTrue(nothing is None)

    def test_pull_pass(self):
        artifactRepo = sb.components.repository.artifactRepo.ArtifactRepo()
        nothing = artifactRepo.pull("artifact", "1.1.0", currentVersion="1.2.0", override=False, user=None, password=None)
        self.assertTrue(nothing is None)

if __name__ == '__main__':
    main()
