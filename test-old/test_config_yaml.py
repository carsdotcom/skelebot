from unittest import TestCase
import skelebot as sb

class TestYaml(TestCase):

    # Setup the Config Object
    def setUp(self):
        args = [sb.config.Param("date", None, None, None)]
        params = [sb.config.Param("env", "e", "local", ["local", "dev", "prod"])]
        defaultJobs = [sb.config.Job("example", "src/jobs/example.job", "EXAMPLE JOB", args, params)]
        kerberos = sb.config.Kerberos("me", "me.keytab", "krb5.conf")
        deploy = sb.config.Deploy("Artifactory", "art.com", "ml", "project")
        artifact = sb.config.Artifact("model", "models/model", deploy)
        artifacts = [artifact]
        plugins = []
        plugins.append(sb.config.Plugin("pluginOne", {"data": "123"}))
        plugins.append(sb.config.Plugin("pluginTwo", {"data": "321"}))
        self.config = sb.config.Config("test", "test project", "0.1", "1.0.0", "me", "me@email.com", "R", kerberos, ["apt-get install pip"], ["stringr", "readr"], [".RData", ".pkl"], defaultJobs, artifacts, ["here:there"], False, plugins)

        self.configDict = {'name': 'test', 'description': 'test project', 'version': '0.1', 'skelebotVersion': '1.0.0', 'maintainer': 'me',
                    'contact': 'me@email.com', 'language': 'R',
                    'kerberos': {'hdfsUser': 'me', 'keytab': 'me.keytab', 'krbConf': 'krb5.conf'},
                    'ephemeral': False,
                    'commands': ['apt-get install pip'],
                    'dependencies': ['stringr', 'readr'],
                    'jobs': [{'name': 'example', 'source': 'src/jobs/example.job', 'help': 'EXAMPLE JOB',
                    'args': [{'name': 'date'}],
                    'params': [{'name': 'env', 'alt': 'e', 'default': 'local', 'choices': ['local', 'dev', 'prod']}]}],
                    'artifacts': [{'name': 'model', 'file': 'models/model',
                    'deploy': {'type': 'Artifactory', 'url': 'art.com', 'repo': 'ml', 'path': 'project'}}],
                    'copy': ['here:there'],
                    'plugins': 
                    [{'name': 'pluginOne', 'config': {'data': '123'}},
                    {'name': 'pluginTwo', 'config': {'data': '321'}}]
                    }

    # Test that the config object is turned into the valid yaml string
    def test_getYaml(self):
        genYaml = self.config.getYaml()
        self.assertTrue("name: test" in genYaml)
        self.assertTrue("description: test project" in genYaml)
        self.assertTrue("version: 0.1" in genYaml)
        self.assertTrue("skelebotVersion: 1.0.0" in genYaml)
        self.assertTrue("maintainer: me" in genYaml)
        self.assertTrue("contact: me@email.com" in genYaml)
        self.assertTrue("language: R" in genYaml)
        self.assertTrue("kerberos:" in genYaml)
        self.assertTrue("  hdfsUser: me" in genYaml)
        self.assertTrue("  keytab: me.keytab" in genYaml)
        self.assertTrue("  krbConf: krb5.conf" in genYaml)
        self.assertTrue("ephemeral: False" in genYaml)
        self.assertTrue("commands:" in genYaml)
        self.assertTrue("- apt-get install pip" in genYaml)
        self.assertTrue("dependencies:" in genYaml)
        self.assertTrue("- stringr" in genYaml)
        self.assertTrue("- readr" in genYaml)
        self.assertTrue("ignore:" in genYaml)
        self.assertTrue("- .RData" in genYaml)
        self.assertTrue("- .pkl" in genYaml)
        self.assertTrue("plugins:" in genYaml)
        self.assertTrue("- name: pluginOne" in genYaml)
        self.assertTrue("  config:" in genYaml)
        self.assertTrue("    data: 123" in genYaml)
        self.assertTrue("- name: pluginTwo" in genYaml)
        self.assertTrue("  config:" in genYaml)
        self.assertTrue("    data: 321" in genYaml)
        self.assertTrue("jobs:" in genYaml)
        self.assertTrue("- name: example" in genYaml)
        self.assertTrue("  source: src/jobs/example.job" in genYaml)
        self.assertTrue("  help: EXAMPLE JOB" in genYaml)
        self.assertTrue("  args:" in genYaml)
        self.assertTrue("  - name: date" in genYaml)
        self.assertTrue("  params:" in genYaml)
        self.assertTrue("  - name: env" in genYaml)
        self.assertTrue("    alt: e" in genYaml)
        self.assertTrue("    default: local" in genYaml)
        self.assertTrue("    choices:" in genYaml)
        self.assertTrue("    - local" in genYaml)
        self.assertTrue("    - dev" in genYaml)
        self.assertTrue("    - prod" in genYaml)
        self.assertTrue("artifacts:" in genYaml)
        self.assertTrue("- name: model" in genYaml)
        self.assertTrue("  file: models/model" in genYaml)
        self.assertTrue("  deploy:" in genYaml)
        self.assertTrue("    type: Artifactory" in genYaml)
        self.assertTrue("    url: art.com" in genYaml)
        self.assertTrue("    repo: ml" in genYaml)
        self.assertTrue("    path: project" in genYaml)
        self.assertTrue("copy:" in genYaml)
        self.assertTrue("- here:there" in genYaml)

    # Test that a dict can be loaded into the YamlClass object
    def test_load(self):
        genConfig = sb.config.Config.load(self.configDict)
        self.assertEqual(self.config.name, genConfig.name)
        self.assertEqual(self.config.description, genConfig.description)
        self.assertEqual(self.config.version, genConfig.version)
        self.assertEqual(self.config.skelebotVersion, genConfig.skelebotVersion)
        self.assertEqual(self.config.maintainer, genConfig.maintainer)
        self.assertEqual(self.config.contact, genConfig.contact)
        self.assertEqual(self.config.language, genConfig.language)
        self.assertEqual(self.config.ephemeral, genConfig.ephemeral)
        self.assertEqual(self.config.commands, genConfig.commands)
        self.assertEqual(self.config.dependencies, genConfig.dependencies)
        self.assertEqual(self.config.kerberos.hdfsUser, genConfig.kerberos.hdfsUser)
        self.assertEqual(self.config.kerberos.keytab, genConfig.kerberos.keytab)
        self.assertEqual(self.config.kerberos.krbConf, genConfig.kerberos.krbConf)
        self.assertEqual(self.config.plugins[0].name, genConfig.plugins[0].name)
        self.assertEqual(self.config.plugins[0].config["data"], genConfig.plugins[0].config["data"])
        self.assertEqual(self.config.plugins[1].name, genConfig.plugins[1].name)
        self.assertEqual(self.config.plugins[1].config["data"], genConfig.plugins[1].config["data"])
        self.assertEqual(self.config.jobs[0].name, genConfig.jobs[0].name)
        self.assertEqual(self.config.jobs[0].source, genConfig.jobs[0].source)
        self.assertEqual(self.config.jobs[0].help, genConfig.jobs[0].help)
        self.assertEqual(self.config.jobs[0].args[0].name, genConfig.jobs[0].args[0].name)
        self.assertEqual(self.config.jobs[0].params[0].name, genConfig.jobs[0].params[0].name)
        self.assertEqual(self.config.jobs[0].params[0].alt, genConfig.jobs[0].params[0].alt)
        self.assertEqual(self.config.jobs[0].params[0].default, genConfig.jobs[0].params[0].default)
        self.assertEqual(self.config.jobs[0].params[0].choices, genConfig.jobs[0].params[0].choices)
        self.assertEqual(self.config.artifacts[0].name, genConfig.artifacts[0].name)
        self.assertEqual(self.config.artifacts[0].file, genConfig.artifacts[0].file)
        self.assertEqual(self.config.artifacts[0].deploy.type, genConfig.artifacts[0].deploy.type)
        self.assertEqual(self.config.artifacts[0].deploy.url, genConfig.artifacts[0].deploy.url)
        self.assertEqual(self.config.artifacts[0].deploy.repo, genConfig.artifacts[0].deploy.repo)
        self.assertEqual(self.config.artifacts[0].deploy.path, genConfig.artifacts[0].deploy.path)

    def test_override(self):
        orig = { "one": 1, "two": 2, "sub": { "three": 3, "four": 4 } }
        over = { "two": 22, "sub": { "three": 33 } }
        expected = { "one": 1, "two": 22, "sub": { "three": 33, "four": 4 } }

        result = sb.yaml.override(orig, over)
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
