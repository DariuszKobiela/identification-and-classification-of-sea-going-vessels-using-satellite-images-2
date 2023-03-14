DATA_PATH = '../data/'
RAW_AIS_ZIP_DATA_PATH = DATA_PATH + '1_raw_AIS_zip_data/'
RAW_AIS_CSV_DATA_PATH = DATA_PATH + '2_raw_AIS_csv_data/'
RAW_ASF_DATA_PATH = DATA_PATH + '3_raw_ASF_data/'
PROCESSED_ASF_DATA_PATH = DATA_PATH + '4_processed_ASF_data/'
PROCESSED_AIS_DATA_PATH = DATA_PATH + '5_processed_AIS_data/'
INTERPOLATED_AIS_DATA_PATH = DATA_PATH + '6_interpolated_AIS_data/'
CUTTED_AND_ANNOTATED_ASF_DATA_PATH = DATA_PATH + '7_cutted_and_annotated_ASF_data/'
FINAL_DATA_PATH = DATA_PATH + '8_final_data/'
FINAL_TEST_DATA_PATH = FINAL_DATA_PATH + 'test/'
FINAL_TRAIN_DATA_PATH = FINAL_DATA_PATH + 'train/'
FINAL_VAL_DATA_PATH = FINAL_DATA_PATH + 'val/'

RESULTS_PATH = '../results/'
PLOTS_PATH = '../plots/'

# constants for AIS data
TIME_WINDOW = 10 # in minutes, +/- how much time to take into consideration between datetime of making the photo
# Use either START, END or MEAN datetime for calculations. MEAN is the preferred option.
USE_END_DATETIME = False
USE_START_DATETIME = False
USE_MEAN_DATETIME = True

# constants for ASF data
CHOSEN_PICTURE_SIZE = 640 # in px # 208 # pictures of example size 1000x1000 will be cutted
SHIP_WIDTH_PX = 50  # 50
SHIP_HEIGHT_PX = 50  # 50
OBJECT_CLASS = 0
FILES_FORMAT_TO_PROCESS = '.png'

#constants for train and test sets creation
STOPFILES = ['.gitkeep', '.ipynb_checkpoints', 'original_picture.txt', 'original_picture.png.aux.xml', 'original_picture.png']
TEST_RATIO = 0.3
VALIDATION_RATIO = 0.3
FORMAT_TO_COPY = 'png'