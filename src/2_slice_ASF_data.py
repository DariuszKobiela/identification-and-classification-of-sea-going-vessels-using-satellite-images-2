from osgeo import gdal
import math
import os
import numpy as np
from skimage import exposure

from src.constants import CUTTED_AND_ANNOTATED_ASF_DATA_PATH, PROCESSED_ASF_DATA_PATH
from src.utils import get_full_data_df
from src.constants import CHOSEN_PICTURE_SIZE


def slice_ASF_pictures(full_data_df, show_logs=False):
    # Slice picture into pieces
    # https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java
    for index, row in full_data_df.iterrows():
        file_name = row['asf_file']
        file_name_no_extension = file_name.strip('.tif')
        if show_logs:
            print(f"File: {index}")
            print(f"File name: {file_name}")
            print(file_name_no_extension)
        working_dir = CUTTED_AND_ANNOTATED_ASF_DATA_PATH + file_name_no_extension + '/'
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)
        in_ds = gdal.Open(PROCESSED_ASF_DATA_PATH + file_name)

        data = in_ds.ReadAsArray()
        # tmp = data[0,:,:]/data[1,:,:]
        tmp = np.divide(data[0, :, :],
                        data[1, :, :],
                        out=np.zeros_like(data[0, :, :]),
                        where=data[1, :, :] != 0)  # only divide nonzeros else 0
        if show_logs:
            print(tmp.shape)
        # ADD 3rd channel to the picture
        tmp_ds = gdal.GetDriverByName('MEM').CreateCopy('', in_ds, 0)
        tmp_ds.AddBand()
        tmp_ds.GetRasterBand(3).WriteArray(tmp)

        # OPTION 1
        data = tmp_ds.ReadAsArray()
        for k in range(3):
            data[k, :, :] = data[k, :, :] / np.nanmax(data[k, :, :])
            # data[k,:,:] = data[k,:,:]*255
            # Histogram stretch
            if show_logs:
                print("mean before", np.mean(data[k, :, :]))
            # data[k,:,:] = exposure.equalize_hist(data[k,:,:])
            data[k, :, :] = exposure.rescale_intensity(data[k, :, :],
                                                       (np.percentile(data[k, :, :], 2), np.percentile(data[k, :, :], 98)))
            # data[k,:,:] = data[k,:,:]*255
            if show_logs:
                print("mean after", np.mean(data[k, :, :]))
            tmp_ds.GetRasterBand(k + 1).WriteArray(data[k, :, :])

        # data = exposure.equalize_hist(data)
        if show_logs:
            print(tmp.shape)
            print(data.shape)
        # convert image to gdal format
        # CUT THE IMAGE WITH 3 channels into tiles
        image_height = row['heightpx']
        image_width = row['widthpx']
        if show_logs:
            print(f"Image_size: {image_width}x{image_height} px")
        image_height = row['heightpx']
        nr_x_edges = math.ceil(image_width / CHOSEN_PICTURE_SIZE)
        nr_y_edges = math.ceil(image_height / CHOSEN_PICTURE_SIZE)
        if show_logs:
            print(f"X_edges: {nr_x_edges}, Y_edges: {nr_y_edges}")
            print(f"All_edges = x_edges*y_edges = {nr_x_edges * nr_y_edges}")
        # translate from TIFF to PNG
        # window = [i*CHOSEN_PICTURE_SIZE, j*CHOSEN_PICTURE_SIZE, CHOSEN_PICTURE_SIZE, CHOSEN_PICTURE_SIZE]
        options_list = [
            '-ot Byte',
            '-of PNG',
            '-b 1',
            '-b 2',
            '-b 3',
            '-scale'
        ]
        options_string = " ".join(options_list)
        kwargs = {
            'format': 'PNG',  # JPEG, PNG, GTIFF
            # 'srcWin': window,
            'options': options_string
        }
        out_ds = gdal.Translate(destName=working_dir + f'original_picture.png',  # .tif, .png
                                srcDS=tmp_ds,
                                **kwargs)
        if show_logs:
            print("original picture done")
        # cut the squares
        subset_number = 0
        for i in range(nr_x_edges):
            for j in range(nr_y_edges):
                subset_number += 1
                window = [i * CHOSEN_PICTURE_SIZE, j * CHOSEN_PICTURE_SIZE, CHOSEN_PICTURE_SIZE, CHOSEN_PICTURE_SIZE]
                # https://stackoverflow.com/questions/50207292/how-to-convert-geotiff-to-jpg-in-python-or-java
                #             options_list = [
                #                 '-ot Byte',
                #                 '-of PNG',
                #                 '-b 1',
                #                 '-b 2',
                #                 '-b 3',
                #                 '-scale'
                #             ]
                kwargs = {
                    'format': 'PNG',  # JPEG, PNG, GTIFF
                    'srcWin': window
                }
                out_ds2 = gdal.Translate(destName=working_dir + f'subset{subset_number}.png',  # .tif, .png
                                         srcDS=out_ds,  # tmp_ds lub out_ds
                                         **kwargs)

                #             # OPTION 2
                #             data=out_ds.ReadAsArray()
                #             tmp_ds2 = gdal.GetDriverByName('MEM').CreateCopy('', out_ds, 0)

                #             if np.isnan(data).any():
                #                 print('nans detected')
                #                 #continue
                #             if np.all(data) == False:
                #                 print('zeros detected')
                #                 #continue
                #             for k in range(3):
                #                 data[k,:,:] = data[k,:,:]/np.nanmax(data[k,:,:])
                #                 data[k,:,:] = data[k,:,:]*255
                #                 data[k,:,:] = exposure.equalize_hist(data[k,:,:])
                #                 tmp_ds2.GetRasterBand(k+1).WriteArray(data[k,:,:])
                #             kwargs = {
                #                 'format': 'PNG', #JPEG, PNG
                #                 'srcWin': window
                #             }

                #             out_ds2 = gdal.Translate(destName = working_dir + f'subset{subset_number}.png',
                #                                     srcDS = tmp_ds2,
                #                                     **kwargs)

                out_width = out_ds2.RasterXSize
                out_height = out_ds2.RasterYSize
                if show_logs:
                    print(f"Out picture {subset_number} width and height: {out_width}x{out_height} px")
        del in_ds
        del out_ds
        print()


full_data_df = get_full_data_df(newest=True, show_logs=False)
slice_ASF_pictures(full_data_df, show_logs=True)
