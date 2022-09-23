import unittest
from skelebot.objects.skeleYaml import SkeleYaml

class TChild(SkeleYaml):

    par_one = None
    par_two = None
    nope = None

    def __init__(self, par_one: int, par_two: int):
        self.par_one = par_one
        self.par_two = par_two
        self.nope = "does not show"

    def toDict(self):
        self.nope = None
        return super().toDict()

class TParent(SkeleYaml):

    childs = None
    fav_child = None
    
    def __init__(self, childs: dict, fav_child: TChild):
        self.childs = childs
        self.fav_child = fav_child

class TestSkeleYaml(unittest.TestCase):

    def test_toDict(self):

        parent = TParent({
                "Jon": TChild(33, 1),
                "Geoffrey": TChild(45, None)
            }, TChild(12, 42))

        res = parent.toDict()
        res_childs = res["childs"]
        res_jon = res_childs["Jon"]
        res_geo = res_childs["Geoffrey"]
        res_fav = res["fav_child"]

        self.assertEqual(res_jon["par_one"], 33)
        self.assertEqual(res_jon["par_two"], 1)
        self.assertNotIn("nope", res_jon)
        self.assertEqual(res_geo["par_one"], 45)
        self.assertNotIn("par_two", res_geo)
        self.assertNotIn("nope", res_geo)
        self.assertEqual(res_fav["par_one"], 12)
        self.assertEqual(res_fav["par_two"], 42)
        self.assertNotIn("nope", res_fav)

if __name__ == '__main__':
    unittest.main()
