import os
import shutil
from pathlib import Path


def clean(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def create_dir(path):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)


def install_ffmpeg():
    pass
