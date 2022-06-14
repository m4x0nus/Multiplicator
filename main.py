import click, os, yaml

@click.command()
@click.option("-c", "--config", default="config.yaml", help="Config yaml file path.", type=click.Path(exists=True))
@click.option('--dry-try', is_flag=True, help="Just check the validity of the config.")

def main(config, dry_try):
    config_file = yaml.full_load(open(config, "r"))
    is_valid(config_file)
    if dry_try:
        return

def is_valid(config_file):
    for skeleton in config_file["skeletons"]:
        if not os.path.isdir(skeleton):
            raise Exception('Skeleton path "' + skeleton + '" is not valid')
    for i in config_file["out"]:
        if not i["skeleton"] in config_file["skeletons"]:
            raise Exception('Skeleton path "' + skeleton + '" is not in skeletons list')

if __name__ == "__main__":
    main()
