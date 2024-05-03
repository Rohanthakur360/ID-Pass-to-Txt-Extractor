import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

ENV = bool(os.environ.get("ENV", False))

if ENV or os.path.exists(".env"):
    from sample_config import *  # noqa
elif os.path.exists("config.py"):
    from config import *  # noq
