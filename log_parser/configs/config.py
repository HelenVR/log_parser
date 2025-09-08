from pydantic import BaseModel
from loguru import logger
import os
import ujson
import yaml


class Api(BaseModel):
    login: str = 'parser'
    password: str = 'parser'
    re_model_file_path: str = './data/re_model.txt'


class Logging(BaseModel):
    save_logs: bool = False
    log_dir: str = 'logs'
    log_rotation_period: str = '1 day'


class Config(BaseModel):
    api: Api
    logging: Logging


def load_config():
    config_file = os.getenv('CONFIG_FILE', 'log_parser/configs/config.yaml')
    with open(config_file, "r") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    logger.info('Config is loaded')
    return Config.parse_raw(ujson.dumps(config))