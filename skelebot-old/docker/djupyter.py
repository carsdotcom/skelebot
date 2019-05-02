import os
from .dname import getImageName
from .dbuild import dbuild

def jupyter(config, args):
    port = config.jupyter.port
    folder = config.jupyter.folder

    # Construct the kerberos init command if required
    krbInit = ""
    if (config.kerberos != None):
        krbInit = "/./krb/init.sh {user} &&".format(user=config.kerberos.hdfsUser)

    allowRoot = ""
    if (config.language == "R"):
        allowRoot = " --allow-root"
    params = "--ip=0.0.0.0 --port=8888{allowRoot}".format(allowRoot=allowRoot)

    status = dbuild(config)

    if (status == 0):
        name = getImageName(config)
        drun = "docker run --rm -p {port}:8888 -iv $PWD:/app {image} /bin/bash -c '{krbInit} jupyter notebook {params} --notebook-dir={folder}'"
        drun = drun.format(port=port, image=name, krbInit=krbInit, params=params, folder=folder)
        os.system(drun)
