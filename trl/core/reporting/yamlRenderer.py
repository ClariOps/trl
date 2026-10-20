import yaml

class NoAnchorDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

class YamlRenderer:
    def __init__(self, manifests, verbose=False):
        self.manifests = manifests
        self.verbose = verbose


    def render(self):
        print(yaml.dump_all(self.manifests, Dumper=NoAnchorDumper, sort_keys=False))