#!/usr/bin/env python3

# File name: COCO.py
#Description: Data processing automation
# Author: Viktor Vodnev
# Date: 10-06-2021

import pandas as pd 
import requests
import os
import json
import argparse
import logging
from zipfile import ZipFile

URL = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
JSON_NAME = "person_keypoints_val2017.json"

def parse_arguments():
    logging.info("Start parsing arguments")
    try:
        parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
        parser.add_argument("-u", type=str, default=None, required=True, help="Enter the link to the file")
        parser.add_argument("-p", type=str, default=None, required=True, help="Enter the path for uploading files")
        args = parser.parse_args()
    except:
        logging.exception("Error reading arguments")
    finally:
        logging.debug("Argument reading completed successfully")

    return args

def get_archive(URL):
    logging.info("Downloading the archive")
    try:
        FILE = requests.get(URL)
        open(str(os.path.dirname(__file__)) + '/archive.zip', 'wb').write(FILE.content)
    except:
        logging.exception("Error downloading archive")
    finally:
        logging.debug("Successful download of the archive")

# check if file exist an return path
def unzip():
    logging.info("The extraction of files from the zip archive starts ")
    try:
        zip_path = os.path.dirname(__file__) + '/archive.zip'
        with ZipFile(zip_path) as z:
            z.extractall(str(os.path.dirname(__file__)))
            for filename in z.namelist():
                if(JSON_NAME in filename):
                    json_path = str(os.path.dirname(__file__)) + '/' + str(filename)
                    return json_path
    except:
        logging.exception("Error extracting files from zip archive")
    finally:
        logging.debug("File extracted successfully")


def open_load(json_path):
    f = open(json_path)
    json_f = json.load(f)
    f.close()
    return json_f


def df_convert(json_file):
    columns  = ["label", "image_name", "image_width", "image_height", "x_min", "y_min", "x_max", "y_max", "image_url"]
    data = []
    df = pd.DataFrame(data, columns=columns)
    images = json_file['images']
    annotations = json_file['annotations']
    categories = json_file['categories']
    for i in range(len(images)):
        for j in range(len(annotations)):
            if(images[i]['id'] == annotations[j]['image_id']):
                df = df.append({'label':categories[0]['name'], 'image_name':images[i]['file_name'], 
                'image_width':images[i]['width'], 'image_height':images[i]['height'], 
                'x_min':annotations[j]['bbox'][0], 'y_min':annotations[j]['bbox'][0] , 
                # x_max = x_min + width of bounding box
                'x_max': round(annotations[j]['bbox'][2] + annotations[j]['bbox'][0], 3),
                # y_max = y_min + height of bounding box
                'y_max': round(annotations[j]['bbox'][3] + annotations[j]['bbox'][1], 3), 
                'image_url':images[i]['coco_url']}, ignore_index=True)
    return df


def df_to_csv(df, csv_path):
    logging.info("Converting date frame to csv file")
    try:
        df.to_csv(csv_path + JSON_NAME.replace('.json', '.csv'), index=False)
        logging.debug("Successful writing to file ")
    except:
        logging.exception("Errors during file convertion")
    finally:
        logging.debug("The file is completely filled with data")


#Removing temporary files
def rm_tmp():
    logging.info("Deleting temporary files ")
    try:
        zip_path = str(os.path.dirname(__file__)) + '/archive.zip'
        folder_path = str(os.path.dirname(__file__)) + '/annotations'
        os.remove(zip_path)
        for f in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, f))
        os.rmdir(folder_path)
        logging.debug("Deleting temporary files was successful")
    except:
        logging.exception("Failed to delete temporary files")


def main():
    logging.basicConfig(level=logging.DEBUG, filename='coco_info.log',
        format='%(asctime)s %(levelname)s:%(message)s')
    #args = parse_arguments()
    get_archive(URL)
    csv_path = "/home/vv173/"
    df = df_convert(open_load(unzip()))
    df_to_csv(df.head(5), csv_path)
    rm_tmp()

if __name__ == '__main__':
    main()
