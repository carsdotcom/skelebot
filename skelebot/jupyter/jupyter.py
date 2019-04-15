import os

def jupyter(config, args):
    port = config.jupyter.port
    folder = config.jupyter.folder

    # Construct the kerberos volume mappings and init command if required
    krbInit = ""
    krb = ""
    if (config.kerberos != None):
        krbInit = "/./krb/init.sh {user} &&".format(user=config.kerberos.hdfsUser)
        krb += "-v {keytab}:/krb/auth.keytab".format(keytab=config.kerberos.keytab)
        if (config.kerberos.cdhJars != None):
            krb += " -v {cdhJars}:/etc/CDH/jars/".format(cdhJars=config.kerberos.cdhJars)

    allowRoot = ""
    if (config.language == "R"):
        allowRoot = " --allow-root"
    params = "--ip=0.0.0.0 --port=8888{allowRoot}".format(allowRoot=allowRoot)

    name = config.name.lower().replace(" ", "-")
    status = 0
    if (not args.skip_build):
        config.generateDockerfile()
        config.generateDockerignore()
        status = status + os.system("docker build -t " + name + " .")
        if (config.ephemeral == True):
            os.remove("Dockerfile")
    if (status == 0):
        drun = "docker run --rm -p {port}:8888 -iv $PWD:/app {krb} {image} /bin/bash -c '{krbInit} jupyter notebook {params} --notebook-dir={folder}'"
        drun = drun.format(port=port, krb=krb, image=name, krbInit=krbInit, params=params, folder=folder)
        os.system(drun)
