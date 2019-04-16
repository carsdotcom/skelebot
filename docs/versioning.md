[Home](index.md) > Versioning

---

# Versioning

Skelebot offers a way to manage the version of your project by keeping it in the skelebot.yaml file.

By default the project will start with version 0.1.0 (initial pre-release version) but this can be changed manually or updated through the
bump command. It is recommended to use the bump command since it will follow the standards of semantic versioning for you.

```
> skelebot bump [major, minor, patch]
```

More information on semantic versioning (when to bump major, minor, and patch) can be found on [semver.org](https://semver.org/).

