import click, os, shutil, yaml

@click.command()
@click.option("-c", "--config", default="config.yaml", help="Config yaml file path.", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Just check the validity of the config.")

def main(config, dry_run):
    config_file = yaml.full_load(open(config, "r"))
    is_valid(config_file)
    if dry_run:
        return
    try:
        shutil.rmtree("out_backup")
    except FileNotFoundError:
        pass
    os.rename(os.path.join("", "out"), os.path.join("", "out_backup"))
    os.makedirs("out", exist_ok=True)
    try:
        for out in config_file["out"]:
            shutil.copytree(os.path.join("skeletons", out["skeleton"]), os.path.join("out", list(out)[0]))
    except Exception as exception:
        shutil.rmtree("out")
        os.rename("out_backup", "out")
        print(exception)
    else:
        shutil.rmtree("out_backup")

def is_valid(config_file):
    for skeleton in config_file["skeletons"]:
        if not os.path.isdir(os.path.join("skeletons", skeleton)):
            raise Exception('Skeleton path "' + os.path.join("skeletons", skeleton) + '" is not valid')
    for i in config_file["out"]:
        if not i["skeleton"] in config_file["skeletons"]:
            raise Exception('Skeleton path "' + skeleton + '" is not in skeletons list')

if __name__ == "__main__":
    main()
