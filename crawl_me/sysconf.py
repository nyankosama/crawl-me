import os, json

URL_OPEN_TIMEOUT = 10
URL_OPEN_RETRY_TIME = 3
MAX_DOWNLOAD_COUNT = 10
MAX_THREAD_COUNT = 40
SPLIT_NUM = 3
RANGE_PART_NUM = 5

AVAILABLE_MODULES = [
    "gamersky",
    "pixiv"
]

PROJECT_METADATA = "project.json"
here = os.path.abspath(os.path.dirname(__file__))
PROJECT_CONF = json.loads(open(os.path.join(here + os.sep + "..", PROJECT_METADATA)).read())
