import pandas as pd
import os

from src.constants import RESULTS_PATH, CUTTED_AND_ANNOTATED_ASF_DATA_PATH, STOPFILES, TEST_RATIO, VALIDATION_RATIO


def calculate_lin_reg_coefficients(x1, y1, x2, y2):
    """
    x is LON (longitude)
    y is LAT (latitude)
    """
    # y = ax + b
    # y1 = a*x1 + b
    # b = y1 - a*x1
    # y2 = a*x2 + y1 - a*x1
    # y2 - y1 = a*x2 - a*x1
    # y2 - y1 = a*(x2-x1)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    return a, b


def categorise_sign_of_time_difference(row):
    if row['time_difference'].days < 0:
        return 0
    return 1


def get_full_data_df(newest=True, given_idx=0, show_logs=False):
    """
    In case when newest=False you have to pass the index
     of the dataframe in the given_idx parameter

    """
    results_list = sorted(os.listdir(RESULTS_PATH), reverse=True)
    idx = 0
    if not newest:
        idx = given_idx
    newest_results_file = results_list[idx]
    full_data_df = pd.read_csv(RESULTS_PATH + newest_results_file, index_col=0)
    if show_logs:
        print(full_data_df)

    return full_data_df


def calculate_px_from_lon2(row, xOrigin, pixelWidth):
    return round((row['LON'] - xOrigin) / pixelWidth)


def calculate_px_from_lat2(row, yOrigin, pixelHeight):
    return round((yOrigin - row['LAT']) / pixelHeight)


def create_train_test_file_splits():
    pictures=list()

    for file in os.listdir(CUTTED_AND_ANNOTATED_ASF_DATA_PATH):
        if not file in STOPFILES:
            pictures.append(file)

    print(pictures)
    total_number_of_pictures = len(pictures)
    print(f"total number_of_folder_pictures: {total_number_of_pictures}")
    print()
    nr_test_pictures = round(TEST_RATIO*total_number_of_pictures)
    print(f"number_of_test_folder_pictures: {nr_test_pictures}")
    nr_train_pictures = total_number_of_pictures - nr_test_pictures
    print(f"number_of_train_folder_pictures: {nr_train_pictures}")
    print()
    nr_val_pictures = round(VALIDATION_RATIO*nr_train_pictures)
    print(f"nr_val_folder_pictures: {nr_val_pictures}")

    test_folders = pictures[0:nr_test_pictures]
    print(f"test_folders: {test_folders}")
    print()
    train_folders = pictures[nr_test_pictures:]
    print(f"train_folders: {train_folders}")
    print()
    val_folders = pictures[nr_test_pictures:nr_test_pictures+nr_val_pictures]
    print(f"val_folders: {val_folders}")

    return train_folders, val_folders, test_folders