import glob
import os
import shutil

from src.constants import FINAL_DATA_PATH, CUTTED_AND_ANNOTATED_ASF_DATA_PATH, INTERPOLATED_AIS_DATA_PATH
from src.utils import delete_contents_of_the_given_folders

# paths = [FINAL_DATA_PATH, CUTTED_AND_ANNOTATED_ASF_DATA_PATH, INTERPOLATED_AIS_DATA_PATH]
paths = [CUTTED_AND_ANNOTATED_ASF_DATA_PATH]

for path in paths:
    delete_contents_of_the_given_folders(path, recursive=True, pattern='txt')  # only delete txt files
    # delete_contents_of_the_given_folders(path, recursive=True, pattern='all')