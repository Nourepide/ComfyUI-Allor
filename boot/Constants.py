import os
from datetime import datetime
from pathlib import Path


class Constants:
    ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TEMPLATE_PATH = ROOT_PATH / "resources/template.json"
    TIMESTAMP_PATH = ROOT_PATH / "resources/timestamp.json"
    CONFIG_PATH = ROOT_PATH / "config.json"
    GIT_PATH = ROOT_PATH / ".git"
    LOG_PATH = ROOT_PATH / f"resources/logs/log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"

    DAY_SECONDS = 24 * 60 * 60
    WEEK_SECONDS = 7 * DAY_SECONDS
    MONTH_SECONDS = 30 * DAY_SECONDS
