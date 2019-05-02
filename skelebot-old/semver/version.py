def bumpVersion(config, mmp):
    oldVersion = config.version
    if (mmp == "patch"):
        version = config.bumpPatch()
    if (mmp == "minor"):
        version = config.bumpMinor()
    if (mmp == "major"):
        version = config.bumpMajor()

    print("Bumped " + mmp + " version. v" + oldVersion + " -> v" + version)

    config.version = version
    return config
