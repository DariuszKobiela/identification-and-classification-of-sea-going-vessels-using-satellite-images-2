import glob
import os
import shutil

from src.constants import FINAL_DATA_PATH, CUTTED_AND_ANNOTATED_ASF_DATA_PATH

#folders = [CUTTED_AND_ANNOTATED_ASF_DATA_PATH]

# file_types = ['jpg', 'tif', 'txt']

# for folder in folders:
#     print(folder)
#     search_string = glob.glob(f'{folder}*/*')
#     print(search_string)
#     for file in search_string:
#         print(os.path.normpath(file))
#         os.remove(file)


files = glob.glob(f'{CUTTED_AND_ANNOTATED_ASF_DATA_PATH}*')
print(files)
for f in files:
    shutil.rmtree(f)


# # clear file structure
# files = glob.glob(f'{CUTTED_AND_ANNOTATED_ASF_DATA_PATH}*/*/*.jpg')
# for f in files:
#     os.remove(f)
# files = glob.glob(f'{CUTTED_AND_ANNOTATED_ASF_DATA_PATH}*/*/*.tif')
# for f in files:
#     os.remove(f)
# files = glob.glob(f'{CUTTED_AND_ANNOTATED_ASF_DATA_PATH}*/*/*.txt')
# for f in files:
#     os.remove(f)


print("works")