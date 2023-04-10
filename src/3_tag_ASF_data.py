from datetime import datetime

import pandas as pd
from osgeo import gdal
import os
from PIL import Image  # PIL library supports only TIF format but not newer TIFF
from tqdm import tqdm
import math

from src.constants import INTERPOLATED_AIS_DATA_PATH, CUTTED_AND_ANNOTATED_ASF_DATA_PATH, FILES_FORMAT_TO_PROCESS, \
    SHIP_WIDTH_PX, SHIP_HEIGHT_PX, OBJECT_CLASS, LOGS_PATH, MAIN_PICTURES_AREAS_PATH
from src.utils import get_full_data_df, calculate_px_from_lon2, calculate_px_from_lat2, BColors


# TODO: calculate separately number of ships after (0,0,0 black pixel color) and (length <30m)

# def create_auxiliary_data_df(asf_df, ais_df, save=True, show_logs=False):
#     full_data_df = asf_df.merge(ais_df, on='date')
#     if show_logs:
#         print(full_data_df)
#     if save:
#         # save your work
#         current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         # print(current_datetime)
#         full_data_df.to_csv(RESULTS_PATH + current_datetime + '_full_data_df.csv')
#
#     return full_data_df

def create_auxiliary_data_df(path, df, asf_file_name, picture_name, area_number):
    # current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # df.to_csv(LOGS_PATH + current_datetime + '_target_area.csv')
    df.to_csv(path + asf_file_name + '_' + picture_name + '_' + str(area_number) + '.csv')


def tag_ASF_pictures(full_data_df, show_logs=False, show_essential_logs=True, tag_main_picture=False):
    TAG_MAIN_PICTURE = tag_main_picture  # takes a lot of time - tag False in order not to tag big picture

    # with tqdm(total = full_data_df.shape[0] * pictures) as pbar:
    for index, row in tqdm(full_data_df.iterrows(), total=full_data_df.shape[0], desc="Tagging ASF pictures"):
        asf_file_name = row['asf_file'].strip(".tif")
        ais_file_name = 'interpolated_processed_' + row['ais_file']
        ais_file_df = pd.read_csv(INTERPOLATED_AIS_DATA_PATH + ais_file_name, index_col=0)
        # HERE STARTS THE DIFFERENCE
        directory = CUTTED_AND_ANNOTATED_ASF_DATA_PATH + asf_file_name
        if show_logs or show_essential_logs:
            print(f"File: {index}")
            print(f"ASF file name: {asf_file_name}")
            print(f"AIS file name: {ais_file_name}")
            print(f'directory: {directory}')

        if os.path.exists(directory):
            pictures = list()
            for file in os.listdir(directory):
                if file.endswith(FILES_FORMAT_TO_PROCESS):
                    pictures.append(file)

            message = BColors.WARNING + "\tPROCESSING MAIN PICTURE MAY TAKE A WHILE..." + BColors.ENDC
            if not TAG_MAIN_PICTURE:
                pictures.remove('original_picture.png')
                message = ''
                # print(pictures)
            if show_logs:
                print(pictures)

            global_ships_counter = 0
            global_ships_after_reduction_counter = 0
            number_of_pictures = len(pictures)
            for area_number, picture in enumerate(pictures): # tqdm(pictures, total=len(pictures), desc="Files processing")
                # processed_files_percentage = round((area_number / number_of_pictures) * 100)
                # print(BColors.WARNING + "\tFILES PROCESSING STATUS: " + str(processed_files_percentage) + "% (" + str(
                #     area_number) + "/" + str(number_of_pictures) + ")" + BColors.ENDC)
                if area_number == 0:
                    print(message)
                print()
                # pbar.update(1)
                picture_name = picture.strip(FILES_FORMAT_TO_PROCESS)
                if show_logs:
                    print(f'picture: {picture}')
                    print(f'picture_name: {picture_name}')
                in_ds = gdal.Open(directory + '/' + picture)
                # print(in_ds)
                image_width = in_ds.RasterXSize
                image_height = in_ds.RasterYSize
                geo_transform = in_ds.GetGeoTransform()

                minx = geo_transform[0]  # minLON
                miny = geo_transform[3] + image_width * geo_transform[4] + image_height * geo_transform[5]  # minLAT
                maxx = geo_transform[0] + image_width * geo_transform[1] + image_height * geo_transform[2]  # maxLON
                maxy = geo_transform[3]  # maxLAT

                xOrigin = geo_transform[0]  # NEEDED
                yOrigin = geo_transform[3]  # NEEDED
                pixelWidth = geo_transform[1]  # NEEDED
                pixelHeight = -geo_transform[5]  # NEEDED
                if show_logs:
                    print(f"image_width: {image_width}, image_height: {image_height}")
                    # print(f"pixel_width: {pixelWidth}, pixel_height: {pixelHeight}")
                    print(f"xOrigin: {xOrigin}, yOrigin: {yOrigin}")
                    # display(ais_file_df.head())

                # Restrict AIS data by the given conditions
                # condition for latitude: between 19.193 and 21.1203
                condition1 = (ais_file_df.LAT > miny) & (ais_file_df.LAT < maxy)
                # condition for latitude: between -157.0894 and -154.4233
                condition2 = (ais_file_df.LON > minx) & (ais_file_df.LON < maxx)
                # final dataframe
                target_area = ais_file_df[condition1 & condition2].copy().reset_index(drop=True)
                # display(target_area)
                # Further work
                if len(target_area) != 0:
                    if show_logs:
                        print('##############')
                        print('SHIPS DETECTED')
                        print('##############')
                    # TODO: if to save empty txt file?
                    # YOLO format do not need empty files for pictures
                    for index, row in target_area.iterrows():
                        target_area['LONpx_X2'] = target_area.apply(
                            lambda row: calculate_px_from_lon2(row, xOrigin, pixelWidth), axis=1)
                        target_area['LATpx_Y2'] = target_area.apply(
                            lambda row: calculate_px_from_lat2(row, yOrigin, pixelHeight), axis=1)

                    if show_logs:
                        print(target_area.head())
                        # print(target_area.columns())
                        print(f"Number of ships founded (including black areas = 0 pixel value): {len(target_area)}")

                    current_file = directory + '/' + picture_name + '.txt'
                    if os.path.exists(current_file):
                        os.remove(current_file)  # remove old files

                    # TODO after adding coordinates
                    if TAG_MAIN_PICTURE and (area_number == 0):
                        create_auxiliary_data_df(MAIN_PICTURES_AREAS_PATH, target_area, asf_file_name, picture_name, area_number)
                    elif area_number % 50 == 0:
                        create_auxiliary_data_df(LOGS_PATH, target_area, asf_file_name, picture_name, area_number)

                    ships_counter = 0
                    for index, row in target_area.iterrows():
                        # Check pixel value - if (0,0,0) then exclude it from the dataset
                        im = Image.open(directory + '/' + picture)  # Can be in many formats.
                        pix = im.load()
                        if show_logs:
                            print(f"Image size: {im.size}")  # Get the width and hight of the image for iterating over
                        try:
                            pixels = pix[row['LONpx_X2'], row['LATpx_Y2']]
                            # print(f"Image pixels values: {pixels}")
                            # print(pixels[0], pixels[1], pixels[2])

                            # if it is dark filling at the edges of the image
                            if pixels[0] == 0 and pixels[1] == 0 and pixels[2] == 0:
                                # DO NOT TAG THE DATA THEN - it is black area
                                if show_logs:
                                    print("0 pixels values - not tagging")
                                continue
                            elif row['Length'] < 3:
                                # # if the ship length is smaller than 20 meters
                                # 12 meters is 1 pixel
                                # DO NOT TAG THE SHIP THEN - it is too small to be seen on the image
                                if show_logs:
                                    print("Ship length is < 3 meters - not tagging")
                                continue

                            ships_counter += 1
                        except:
                            print("IndexError: image index out of range")
                            continue

                        # CHECK IF VALUE IS NAN (EMPTY) - IF SO, DO NOT TAG
                        if math.isnan(row['Length']):
                            continue

                        object_class = 0
                        # # CLASSES CUTS = [110m, 265m]
                        # if row['Length'] < 111:
                        #     object_class = 0  # small ship
                        # elif row['Length'] < 266:
                        #     object_class = 1  # medium ship
                        # else:
                        #     object_class = 2  # big ship

                        # # CLASSES CUTS = [12m, 17m, 26m, 230m]
                        # if row['Length'] < 12:
                        #     object_class = 0
                        # elif row['Length'] < 18:
                        #     object_class = 1
                        # elif row['Length'] < 27:
                        #     object_class = 2
                        # elif row['Length'] < 231:
                        #     object_class = 3
                        # else:
                        #     object_class = 4

                        file_object = open(current_file, 'a')
                        # OBJECT_CLASS, SHIP_WIDTH_PX, SHIP_HEIGHT_PX
                        # print("before normalization")
                        # print("LONpx_X2", row['LONpx_X2'])
                        # print("LATpx_Y2", row['LATpx_Y2'])
                        X_CENTER_AXIS_VALUE = row['LONpx_X2']
                        Y_CENTER_AXIS_VALUE = row['LATpx_Y2']
                        # print(OBJECT_CLASS, X_CENTER_AXIS_VALUE, Y_CENTER_AXIS_VALUE, SHIP_WIDTH_PX, SHIP_HEIGHT_PX)
                        # print("after normalization")
                        # X_CENTER_AXIS_VALUE = (X_CENTER_AXIS_VALUE + SHIP_WIDTH_PX/2) / image_width
                        # Y_CENTER_AXIS_VALUE = (Y_CENTER_AXIS_VALUE + SHIP_HEIGHT_PX/2) / image_height
                        X_CENTER_AXIS_VALUE = X_CENTER_AXIS_VALUE / image_width
                        Y_CENTER_AXIS_VALUE = Y_CENTER_AXIS_VALUE / image_height
                        SHIP_WIDTH_normalized = SHIP_WIDTH_PX / image_width
                        SHIP_HEIGHT_normalized = SHIP_HEIGHT_PX / image_height
                        # print(OBJECT_CLASS, X_CENTER_AXIS_VALUE, Y_CENTER_AXIS_VALUE, SHIP_WIDTH_normalized, SHIP_HEIGHT_normalized)
                        string_to_write = f"{object_class} {X_CENTER_AXIS_VALUE} {Y_CENTER_AXIS_VALUE} {SHIP_WIDTH_normalized} {SHIP_HEIGHT_normalized}\n"
                        file_object.write(string_to_write)
                        # Close the file
                        file_object.close()

                    if picture == 'original_picture.png':
                        global_ships_counter = len(target_area)
                        global_ships_after_reduction_counter = ships_counter

                    if show_logs:
                        print(f"Number of ships founded (including black areas = 0 pixel value): {len(target_area)}")
                        print(f"Number of ships founded after excluding black areas == 0 pixel value: {ships_counter}")
                else:
                    if show_logs:
                        print()
                    # print('Sorry, no ships on the selected area')
                    # file_object = open(directory + '/' + picture_name + '.txt', 'a')
                    # file_object.close()
                print()
        else:
            print('ERROR!! no picture data')
            print('TRY ANNOTATION AGAIN')
            continue

        if TAG_MAIN_PICTURE and show_essential_logs:
            print(f"Number of ships founded (including black areas = 0 pixel value): {global_ships_counter}")
            print(f"Number of ships founded after excluding (black areas == 0 pixel value) and (ship length < 30 m): {global_ships_after_reduction_counter}")


full_data_df = get_full_data_df(newest=True, show_logs=False)
# tag_ASF_pictures(full_data_df, show_logs=False, show_essential_logs=True, tag_main_picture=True)
tag_ASF_pictures(full_data_df, show_logs=False, show_essential_logs=True, tag_main_picture=False)
