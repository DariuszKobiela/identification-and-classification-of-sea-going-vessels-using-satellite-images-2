# Import Libraries
import sys
sys.path.append('C:/Python34/virtenv/Lib/snappy')  # NECESSARY FOR SNAPPY

import os
os.system('color')  # to get the ANSI codes working on windows

import snappy
from snappy import ProductIO, Product, ProductData, ProductUtils, String
from snappy import HashMap, GPF, Product, ProductIO, ProductUtils, WKTReader
from src.constants import LOS_ANGELES_WKT, PROCESSED_ASF_DATA_PATH, RAW_ASF_DATA_PATH_BATCH0, RAW_ASF_DATA_PATH_BATCH1, RAW_ASF_DATA_PATH_BATCH2, RAW_ASF_DATA_PATH_BATCH3


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
# ANSI escape sequences. Python code from the Blender build scripts:
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ImageSubset(input_file, wkt, save=False, file_saving_location=PROCESSED_ASF_DATA_PATH, file_saving_format='BEAM-DIMAP'):
    print('\tSubsetting...')
    parameters = HashMap()
    geom = WKTReader().read(wkt)
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geom)
    output_file = GPF.createProduct('Subset', parameters, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


def LandSeaMask(input_file, save=False, file_saving_location=PROCESSED_ASF_DATA_PATH, file_saving_format='BEAM-DIMAP'):
    print('\tLand/Sea Masking...')
    params = HashMap()
    params.put('useSRTM', True)
    params.put('landMask', True)
    params.put('shorelineExtension', '40')
    params.put('sourceBands', 'Intensity_VV, Intensity_VH')
    output_file = GPF.createProduct('Land-Sea-Mask', params, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


def GeometricTerrainCorrection(input_file, save=True, file_saving_location=PROCESSED_ASF_DATA_PATH, file_saving_format='GeoTIFF'):
    print('\tRadar Geometric Terrain correction...')
    # https://forum.step.esa.int/t/s1a-product-terrain-correction/27599/10
    # DETAILED DOCUMENTATION
    # print(subprocess.Popen(['gpt', '-h', 'Terrain-Correction'], stdout=subprocess.PIPE,
    #                        universal_newlines=True).communicate()[0])
    parameters = HashMap()
    parameters.put('sourceBandNames', 'Intensity_VV, Intensity_VH')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('demName', 'Copernicus 30m Global DEM')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('saveSelectedSourceBand', True)
    parameters.put('mapProjection', 'WGS84(DD)')
    parameters.put('nodataValueAtSea', False)
    parameters.put('maskOutAreaWithoutElevation', False)
    output_file = GPF.createProduct("Terrain-Correction", parameters, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


# Set Path to Input Satellite Data
# input_path = r'C:\Users\user\PycharmProjects\identification-and-classification-of-sea-going-vessels-using-satellite-images\data\3_raw_ASF_data'
# input_path = r'../data/3_raw_ASF_data'
# .dim is BEAM-DIMAP format, native to snap
# our final destination format is 'GeoTIFF'

#################################################################################################################
# CHOOSE DATA BATCH
raw_asf_data_path = RAW_ASF_DATA_PATH_BATCH0
################################################################################################################

sentinel_files = os.listdir(raw_asf_data_path)
number_of_sentinel_files = len(sentinel_files)
print(sentinel_files)

for count, sentinel_file in enumerate(sentinel_files):
    processed_files_percentage = round((count/number_of_sentinel_files) * 100)
    print()
    print(BColors.WARNING + "\tFILES PROCESSING STATUS: " + str(processed_files_percentage) + "% (" + str(count) + "/" + str(number_of_sentinel_files) + ")" + BColors.ENDC)
    print()
    file_saving_location = PROCESSED_ASF_DATA_PATH + "\\" + sentinel_file.strip(".zip")
    sentinel_1 = ProductIO.readProduct(raw_asf_data_path + "\\" + sentinel_file)
    bands = list(sentinel_1.getBandNames())
    print("\tProcessing " + str(sentinel_1) + ", initial bands " + str(bands))
    subset_sentinel1 = ImageSubset(sentinel_1, LOS_ANGELES_WKT, save=False, file_saving_location=file_saving_location, file_saving_format='BEAM-DIMAP')
    masked_sentinel1 = LandSeaMask(subset_sentinel1, save=False, file_saving_location=file_saving_location, file_saving_format='BEAM-DIMAP')
    terrain_corrected_sentinel1 = GeometricTerrainCorrection(masked_sentinel1, save=True, file_saving_location=file_saving_location, file_saving_format='GeoTIFF')
    print("\tFile " + str(terrain_corrected_sentinel1) + " saved into " + str(file_saving_location))

print("\tALL ASF data processed via ESA SNAPPY")



