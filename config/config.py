from pathlib import Path

import yaml

HERE = Path(__file__).parent
CONF_PATH = HERE / "conf.yaml"

if CONF_PATH.is_file():

    with open( CONF_PATH, "r") as f:
        config = yaml.load(f)

    nb_days = config['nb_days']
    url = config['url']
    save = config['save']
    dataset_path = config['dataset']