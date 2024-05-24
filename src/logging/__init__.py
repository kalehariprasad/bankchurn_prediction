import logging
import os
from datetime import datetime
import pathlib

curr_dir = pathlib.Path(__file__)
home_dir = curr_dir.parent.parent.parent
logs_folder = home_dir.as_posix() + '/logs'

os.makedirs(logs_folder, exist_ok=True)

current_time_stamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

log_file_name = f"log_{current_time_stamp}.log"

log_file_path = os.path.join(logs_folder, log_file_name)

logging.basicConfig(filename=log_file_path, filemode="w",
                    format='[%(asctime)s] %(name)s - %(levelname)s %(message)s',
                    level=logging.INFO)