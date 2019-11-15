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
        parts = version.split(".")
        self.major = parts[0]
        self.minor = parts[1]
        self.patch = parts[2]

    def __str__(self):
        return "{maj}.{min}.{pat}".format(maj=self.major, min=self.minor, pat=self.patch)

    def __lt__(self, other):
        lt = False
        if (self.major < other.major) or ((self.major == other.major) and ((self.minor < other.minor) or ((self.minor == other.minor) and (self.patch < other.patch)))):
            lt = True

        return lt

    def __eq__(self, other):
        eq = True
        if (self.patch != other.patch) or (self.minor != other.minor) or (self.major != other.major):
            eq = False

        return eq

    def __le__(self, other):
        le = False
        if (self < other) or (self == other):
            le = True

        return le

    def isBackwardCompatible(self, semver):
        """Determine whether this Semver backword compatible with the Semver provided"""

        compat = False
        if (self.major == semver.major) and (self >= semver):
            compat = True

        return compat

