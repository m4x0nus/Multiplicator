import click, os, shutil, yaml

@click.command()
@click.option("-c", "--config", default="config.yaml", help="Config yaml file path.", type=click.Path(exists=True))
@click.option('--dry-try', is_flag=True, help="Just check the validity of the config.")

def main(config, dry_try):
    config_file = yaml.full_load(open(config, "r"))
    is_valid(config_file)
    if dry_try:
        return
    try:
        shutil.rmtree('out_backup')
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname("\out_backup"), exist_ok=True)
    shutil.copytree("out", "out_backup")
    try:
        pass #Main part
    except Exception as exception:
        shutil.rmtree('out')
        os.rename('out_backup', 'out')
        print(exception)
    else:
        shutil.rmtree('out_backup')

def is_valid(config_file):
    for skeleton in config_file["skeletons"]:
        if not os.path.isdir(skeleton):
            raise Exception('Skeleton path "' + skeleton + '" is not valid')
    for i in config_file["out"]:
        if not i["skeleton"] in config_file["skeletons"]:
            raise Exception('Skeleton path "' + skeleton + '" is not in skeletons list')

if __name__ == "__main__":
    main()
