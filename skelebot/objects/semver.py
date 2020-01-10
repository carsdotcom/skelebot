class Semver():
    """
    Semver Class

    Object to translate a semantic version string into an object with separate values for major, minor, and patch that allows for operations to
    be performed such as comparing two Semvers.
    """

    major = None
    minor = None
    patch = None

    def __init__(self, version):
        """ Initialize the Major, Minor, and Patch numbers of a semantic version number """
        parts = version.split(".")
        self.major = parts[0]
        self.minor = parts[1]
        self.patch = parts[2]

    def __str__(self):
        """ When converting to a String the format should read as major.minor.patch """
        return "{maj}.{min}.{pat}".format(maj=self.major, min=self.minor, pat=self.patch)

    def __lt__(self, other):
        """ Check if this semver is smaller (less recent) than another semver """
        lt = False
        if (self.major < other.major) or ((self.major == other.major) and ((self.minor < other.minor) or ((self.minor == other.minor) and (self.patch < other.patch)))):
            lt = True

        return lt

    def __eq__(self, other):
        """ Check if this semver is exactly equal to another semver """
        eq = True
        if (self.patch != other.patch) or (self.minor != other.minor) or (self.major != other.major):
            eq = False

        return eq

    def __le__(self, other):
        """ Check if this semver is larger (more recent) than another semver """
        le = False
        if (self < other) or (self == other):
            le = True

        return le

    def isBackwardCompatible(self, semver):
        """
        Determine whether this Semver is backward compatible with the Semver provided

        For this semver to be backward compatible with another the Major version of each must be
        the same and this semver must be at least as large (at least as recent) as the one provided
        """

        compat = False
        if (self.major == semver.major) and (self >= semver):
            compat = True

        return compat

