import pandas as pd
from osgeo import gdal
import math
import os
import glob
from PIL import Image # PIL library supports only TIF format but not newer TIFF
import numpy as np
import shutil

from src.constants import CUTTED_AND_ANNOTATED_ASF_DATA_PATH, FINAL_DATA_PATH, FORMAT_TO_COPY, FINAL_TEST_DATA_PATH, \
    FINAL_TRAIN_DATA_PATH, FINAL_VAL_DATA_PATH
from src.utils import create_train_test_file_splits


def copy_pictures_and_labels(source_path, source_images_folders, destination_path_images, destination_path_labels,
                             destination_format, counter):
    source_path = source_path
    source_images_folders = source_images_folders
    destination_path_images = destination_path_images
    destination_path_labels = destination_path_labels
    destination_format = destination_format
    image_counter = counter
    labels_counter = counter
    print(destination_path_labels)

    for folder in source_images_folders:
        # print()
        # print(folder)
        # choose only files with txt annotations
        # print(os.listdir(source_path + folder))
        # print()
        labels = list()
        images = list()
        for file in os.listdir(source_path + folder):
            if file.endswith(".txt"):
                labels.append(file)
                image_file = file.replace(".txt", ".png")
                images.append(image_file)
        # print(f"images: {images}")
        # print(f"labels: {labels}")
        # labels
        for file in labels:
            src = source_path + '/' + folder + '/' + file
            # print(f"src: {src}")
            dst = destination_path_labels + str(labels_counter) + '.txt'  # folder + file
            # print(f"dst: {dst}")
            shutil.copy(src, dst)
            labels_counter += 1
        # pictures
        counter = counter
        for file in images:
            src = source_path + '/' + folder + '/' + file
            # print(f"src: {src}")
            dst = destination_path_images + str(image_counter) + '.' + destination_format  # folder + file
            # print(f"dst: {dst}")
            shutil.copy(src, dst)
            image_counter += 1

    return image_counter

train_folders, val_folders, test_folders = create_train_test_file_splits()

# clear file structure
files = glob.glob(f'{FINAL_DATA_PATH}*/*/*.jpg')
for f in files:
    os.remove(f)
files = glob.glob(f'{FINAL_DATA_PATH}*/*/*.png')
for f in files:
    os.remove(f)
files = glob.glob(f'{FINAL_DATA_PATH}*/*/*.tif')
for f in files:
    os.remove(f)
files = glob.glob(f'{FINAL_DATA_PATH}*/*/*.txt')
for f in files:
    os.remove(f)

# start counting
counter = 0
# TEST PICTURES
counter = copy_pictures_and_labels(source_path=CUTTED_AND_ANNOTATED_ASF_DATA_PATH,
                                   source_images_folders=test_folders,
                                   destination_path_images=FINAL_TEST_DATA_PATH + 'images/',
                                   destination_path_labels=FINAL_TEST_DATA_PATH + 'labels/',
                                   destination_format=FORMAT_TO_COPY,
                                   counter=counter)
print(f"counter: {counter}")
counter = 0
# TRAIN PICTURES
counter = copy_pictures_and_labels(source_path=CUTTED_AND_ANNOTATED_ASF_DATA_PATH,
                                   source_images_folders=train_folders,
                                   destination_path_images=FINAL_TRAIN_DATA_PATH + 'images/',
                                   destination_path_labels=FINAL_TRAIN_DATA_PATH + 'labels/',
                                   destination_format=FORMAT_TO_COPY,
                                   counter=counter)
print(f"counter: {counter}")
counter = 0
# VALIDATION PICTURES
counter = copy_pictures_and_labels(source_path=CUTTED_AND_ANNOTATED_ASF_DATA_PATH,
                                   source_images_folders=val_folders,
                                   destination_path_images=FINAL_VAL_DATA_PATH + 'images/',
                                   destination_path_labels=FINAL_VAL_DATA_PATH + 'labels/',
                                   destination_format=FORMAT_TO_COPY,
                                   counter=counter)
print(f"counter: {counter}")

