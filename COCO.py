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

def parse_arguments():
    logging.info("Start parsing arguments ")
    try:
        parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
        parser.add_argument("-u", type=str, default=None, required=True, help="Enter the link to the file")
        parser.add_argument("-p", type=str, default=None, required=True, help="Enter the path for uploading files")
        args = parser.parse_args()
    except:
        logging.exception("Error reading arguments ")
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


def file_path():
    logging.info("The extraction of files from the zip archive starts ")
    try:
        jsons_path = []
        zip_path = os.path.dirname(__file__) + '/archive.zip'
        with ZipFile(zip_path) as z:
            z.extractall(str(os.path.dirname(__file__)))
            for filename in z.namelist():
                if(filename[-1] != '/'):
                    jsons_path.append(str(os.path.dirname(__file__)) + '/' + str(filename))
    except:
        logging.exception("Error extracting files from zip archive ")
    finally:
        logging.debug("File extraction successfully")
    return jsons_path

def open_load():
    json_f = []
    for path in file_path():
        f = open(path)
        json_f.append(json.load(f))
        f.close()

    return json_f

def df_convert(jfile):
    
    columns  = ["label", "image_name", "image_width", "image_height", "x_min", "y_min", "x_max", "y_max", "image_url"]
    data = []
    df = pd.DataFrame(data, columns=columns)
    images = jfile['images']
    annotations = jfile['annotations']
    categories = jfile['categories']

    for i in range(len(images)):
        for j in range(len(annotations)):
            if(images[i]['id'] == annotations[j]['image_id']):
                for k in range(len(categories)):
                    if(annotations[j]['category_id'] == categories[k]['id']):
                        df = df.append({'label':categories[k]['name'], 'image_name':images[i]['file_name'], 
                        'image_width':images[i]['width'], 'image_height':images[i]['height'], 
                        'x_min':annotations[j]['bbox'][0], 'y_min':annotations[j]['bbox'][0] , 
                        'x_max': round(annotations[j]['bbox'][2] - annotations[j]['bbox'][0], 3), 
                        'y_max': round(annotations[j]['bbox'][3] - annotations[j]['bbox'][1], 3), 
                        'image_url':images[i]['coco_url']}, ignore_index=True)
    return df

def name_parse():
    names = []
    for path in file_path():
        names.append((path.split('/')[-1]).split('.')[0])
    return names

def df_to_csv(df, path):
    logging.info("Converting date frame to csv file")
    try:
        names = name_parse()
        for j in range(len(names)):
            df.to_csv(path + names[j] + '.csv', index=False)
        logging.debug("Successful writing to file ")
    except:
        logging.exception("Errors during file creation")
    finally:
        logging.debug("The file is completely filled with data")


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
    args = parse_arguments()
    URL = args.u
    UP_PATH = args.p
    get_archive(URL)
    jsons = open_load()
    for i in range(len(jsons)):
        df = df_convert(jsons[i])
        df_to_csv(df, UP_PATH)
    rm_tmp()


if __name__ == '__main__':
    main()