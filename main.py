config_name = "config.yaml"

import yaml, os

def is_valid(config):
    for skeleton in config["skeletons"]:
        if not os.path.isdir(skeleton):
            raise Exception('Skeleton path "' + skeleton + '" is not valid')
    for i in config["out"]:
        if not i["skeleton"] in config["skeletons"]:
            raise Exception('Skeleton path "' + skeleton + '" is not in skeletons list')

def main():
    config = yaml.full_load(open(config_name, "r"))
    print(config)
    is_valid(config)

if __name__ == "__main__":
    main()
