from typing import List, Type
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=".flaskenv", verbose=True)


class Config:
    CONFIG_NAME = "base"
    DEBUG = False
    basedir = os.path.dirname(os.path.abspath(__file__))


class DevelopmentConfig(Config):

    CONFIG_NAME = "dev"
    DEBUG = True
    ENV = "dev"

class ProductionConfig(Config):
    
    CONFIG_NAME = "prod"
    DEBUG = False
    ENV = "prod"



EXPORT_CONFIGS: List[Type[Config]] = [
    DevelopmentConfig,
    ProductionConfig
]
config_by_name = { cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS }