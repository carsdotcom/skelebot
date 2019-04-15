from unittest import TestCase
import skelebot as sb

class TestDockerDname(TestCase):

    # Test that the name is pulled out and cleaned up properly
    def test_getImageName(self):
        cfg = sb.config.Config("All My Code", "proj", "2", "1", "me", "me", "R", None, None, None, None, None, None, None, "False", None)
        name = sb.dname.getImageName(cfg)
        self.assertEqual("all-my-code", name)

if __name__ == '__main__':
    unittest.main()
