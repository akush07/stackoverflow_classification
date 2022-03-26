import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.helper import read_yaml, create_directories
from src.utils.helper import process_posts
import random


workflow_step = "Stage 2: prepare data"

logpath = r'C:\Users\ASUS\OneDrive\Projects\stackoverflow_classification\logs'

logging.basicConfig(
    filename=os.path.join(logpath, 'running_logs.log'),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def data_preparation(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    local_data_dir = config["source_download_dirs"]["data_dir"]
    data_filename = config["source_download_dirs"]["data_file"]
    input_data = os.path.join(local_data_dir, data_filename)

    split = params["prepare"]["split"]
    seed = params["prepare"]["seed"]

    random.seed(seed)

    artifacts = config["artifacts"]
    prepared_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DATA"])
    create_directories([prepared_data_dir_path])

    train_data_path = os.path.join(prepared_data_dir_path, artifacts["TRAIN_DATA"])
    test_data_path = os.path.join(prepared_data_dir_path, artifacts["TEST_DATA"])

    encode = "utf8"
    with open(input_data, encoding=encode) as f_in:
        with open(train_data_path, "w", encoding=encode) as f_out_train:
            with open(test_data_path, "w", encoding=encode) as f_out_test:
                process_posts(f_in, f_out_train, f_out_test, "<python>", split)



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="../../configs/config.yaml")
    args.add_argument("--params", "-p", default="../../params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {workflow_step} started <<<<<")
        data_preparation(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {workflow_step} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e