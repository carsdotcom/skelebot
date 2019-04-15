import os
from .dname import getImageName
from .dbuild import dbuild

def dexec(config):
    status = dbuild(config)

    # Run the Container interactively with bash
    if (status == 0):
        name = getImageName(config)
        drun = "docker run --rm -it {image} /bin/bash".format(image=name)
        os.system(drun)
