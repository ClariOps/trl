import yaml

class NoAnchorDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

class YamlRenderer:
    def __init__(self, manifests):
        self.manifests = manifests


    def render(self):
        return yaml.dump_all(self.manifests, Dumper=NoAnchorDumper, sort_keys=False)