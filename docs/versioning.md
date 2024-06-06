[Home](index.md)

---

# Versioning

Skelebot offers a way to manage the version of your project by keeping it in a standalone `VERSION` file in the project folder.

The reason this file stands alone is to allow for the version to be read more easily from a variety of different sources (GitHub README, python pyproject file, etc.).

By default the project will start with version 0.1.0 (initial pre-release version) but this can be changed manually or updated through the bump command. It is recommended to use the bump command since it will follow the standards of semantic versioning for you.

```
> skelebot bump [major, minor, patch]
```

More information on semantic versioning (when to bump major, minor, and patch) can be found on [semver.org](https://semver.org/).

---

<center><< <a href="environments.html">Environments</a>  |  <a href="publishing.html">Publishing</a> >></center>
