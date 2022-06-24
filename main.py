import click, os, sys, shutil, glob, yaml, jinja2

@click.command()
@click.option("-c", "--config", default="config.yaml", help="Config yaml file path.", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Just check the validity of the config.")

def main(config, dry_run):
    config_file = yaml.full_load(open(config, "r"))
    is_valid(config_file)
    if dry_run:
        return
    make_backup()
    try:
        for section in config_file["out"]:
            section_name = str(list(section)[0])
            shutil.copytree(os.path.join("skeletons", section["skeleton"]), os.path.join("out", section_name))
            if "var" in section:
                if "var" in config_file:
                    var = {**config_file["var"], **section["var"]}
                else:
                    var = section["var"]
            else:
                if "var" in config_file:
                    var = config_file["var"]
                else:
                    var = {}
            var["section_name"] = section_name
            for template_path in glob.glob(os.path.join("out", section_name, "**", "*.template"), recursive=True):
                template = jinja2.Template(open(template_path).read())
                f = open(os.path.splitext(template_path)[0], "w")
                f.write(template.render(var))
                f.close()
                os.remove(template_path)
    except Exception as exception:
        restore_backup()
        print(exception)
    else:
        erase_backup()

def make_backup():
    try:
        try:
            shutil.rmtree("out_backup")
        except FileNotFoundError:
            pass
        os.rename(os.path.join("", "out"), os.path.join("", "out_backup"))
    except FileNotFoundError:
        os.makedirs("out", exist_ok=True)
    else:
        os.makedirs("out", exist_ok=True)

def restore_backup():
    shutil.rmtree("out")
    os.rename("out_backup", "out")

def erase_backup():
    try:
        shutil.rmtree("out_backup")
    except FileNotFoundError:
        pass

def is_valid(config_file):
    exceptions = ""
    for skeleton in config_file["skeletons"]:
        if not os.path.isdir(os.path.join("skeletons", skeleton)):
            exceptions += 'Skeleton path "' + os.path.join("skeletons", skeleton) + '" is not valid \n'
    for section in config_file["out"]:
        if not section["skeleton"] in config_file["skeletons"]:
            exceptions += 'Skeleton path "' + skeleton + '" is not in skeletons list'
    if exceptions != "":
        sys.exit(exceptions)

if __name__ == "__main__":
    main()
