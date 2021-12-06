"""Docker Command Builder"""

EP_COMMAND = " {command} {image} {parameters}"
EX_COMMAND = " {image} /bin/bash -c \"{command}\""

class SaveCommandBuilder():
    cmd = None
    image = None

    def __init__(self, cmd, image):
        self.image = image
        self.cmd = cmd + " save"

    def set_output(self, filename):
        self.cmd += " -o {}".format(filename)
        return self

    def build(self):
        self.cmd += " {}".format(self.image)
        return self.cmd

class PushCommandBuilder():
    cmd = None

    def __init__(self, cmd, image):
        self.cmd = cmd + " push {}".format(image)

    def set_tag(self, tag):
        self.cmd += ":{}".format(tag)
        return self

    def build(self):
        return self.cmd

class RunCommandBuilder():
    cmd = None
    image = None
    entrypoint = False
    parameters = None

    def __init__(self, cmd, image):
        self.image = image
        self.cmd = cmd + " run"

    def set_name(self, name):
        self.cmd += " --name {}".format(name)
        return self

    def set_rm(self):
        self.cmd += " --rm"
        return self

    def set_entrypoint(self, parameters):
        self.parameters = parameters
        self.entrypoint = True
        self.cmd += " --entrypoint"
        return self
    
    def set_gpu(self):
        self.cmd += " --gpus all --ipc=host"
        return self

    def set_mode(self, mode):
        self.cmd += " -{}".format(mode)
        return self

    def set_port(self, port):
        self.cmd += " -p {}".format(port)
        return self

    def set_volume(self, volume):
        self.cmd += " -v {}".format(volume)
        return self

    def set_params(self, params):
        self.cmd += " {}".format(params)
        return self

    def build(self, command):
        if (self.entrypoint):
            job_command = EP_COMMAND.format(command=command, image=self.image, parameters=self.parameters)
            self.cmd += job_command
        else:
            job_command = EX_COMMAND.format(command=command, image=self.image)
            self.cmd += job_command

        return self.cmd

class DockerCommandBuilder():
    cmd = None

    def __init__(self, host=None):
        self.cmd = "docker"
        if host is not None:
            print("Executing Docker on Host {}".format(host))
            self.cmd += " -H {}".format(host)

    def login(self, hub):
        self.cmd += " login {}".format(hub)
        return self.cmd

    def build(self, image):
        self.cmd += " build -t {} .".format(image)
        return self.cmd

    def tag(self, src, image, tag):
        self.cmd += " tag {src} {image}:{tag}".format(src=src, image=image, tag=tag)
        return self.cmd

    def save(self, image):
        return SaveCommandBuilder(self.cmd, image)

    def push(self, image):
        return PushCommandBuilder(self.cmd, image)

    def run(self, image):
        return RunCommandBuilder(self.cmd, image)
