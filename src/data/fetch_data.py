
import argparse
import os
import logging
from src.utils.helper import read_yaml, create_directories
import urllib.request as req


workflow_step = 'Stage 1: Get Data'

logpath = r'logs'

os.makedirs(logpath, exist_ok=True)
with open('running_logs.log','a') as f:
    pass

logging.basicConfig(
    filename=os.path.join(logpath, 'running_logs.log'),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    )

def get_data(config):
    source_data_url = config["source_data_url"]
    local_data_dir = config['source_download_dirs']['data_dir']
    create_directories([local_data_dir])

    data_filename = config["source_download_dirs"]["data_file"]
    local_data_filepath = os.path.join(local_data_dir, data_filename)

    logging.info("Starting Download..")
    filename, header = req.urlretrieve(source_data_url, local_data_filepath)
    logging.info("Downloading completed")
    logging.info("Download file is present at: {filename}")
    logging.info(f"Download headers: \n{header}")

if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c", default="../../configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {workflow_step} started <<<<<")
        config = read_yaml(parsed_args.config)
        get_data(config)
        logging.info(f">>>>> stage {workflow_step} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e