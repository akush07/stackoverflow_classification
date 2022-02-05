import os
import yaml
import logging
import time
import pandas as pd
import json
from tqdm import tqdm
import random
import xml.etree.ElementTree as ET
import re
import joblib
import scipy.sparse as sparse
import numpy as np


def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content

def create_directories(path_to_directories: list) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")

def get_df(path_to_data: str, sep: str="\t") -> pd.DataFrame:
    df = pd.read_csv(
        path_to_data,
        encoding="utf-8",
        header=None,
        delimiter=sep,
        names=["id", "label", "text"]
    )
    logging.info(f"The input data frame {path_to_data} size is {df.shape}\n")
    return df



def process_posts(f_in, f_out_train, f_out_test, target_tag, split):

    line_num = 1
    for line in tqdm(f_in):
        try:
            f_out = f_out_train if random.random() > split else f_out_test
            attr = ET.fromstring(line).attrib

            pid = attr.get('Id', "")
            label = 1 if target_tag in attr.get('Tags', "") else 0
            title = re.sub(r"\s+", " ", attr.get('Title', "")).strip()
            body = re.sub(r"\s+", " ", attr.get('Body', "")).strip()
            text = title + " " + body

            f_out.write(f"{pid}\t{label}\t{text}\n")
            line_num += 1
        except Exception as e:
            msg = f"Skipping the broken line {line_num}: {e}\n"
            logging.exception(msg)

def save_matrix(df, matrix, out_path):
    id_matrix = sparse.csr_matrix(df.id.astype(np.int64)).T
    label_matrix = sparse.csr_matrix(df.label.astype(np.int64)).T

    result = sparse.hstack([id_matrix, label_matrix, matrix], format="csr")

    joblib.dump(result, out_path)
    msg = f"The output matrix saved at: {out_path} of the size: {result.shape} and data type: {result.dtype}"
    logging.info(msg)