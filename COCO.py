#!/usr/bin/env python3

import pandas as pd 
import requests
import os
import json
import argparse
from zipfile import ZipFile

URL1 = "http://images.cocodataset.org/annotations/image_info_test2017.zip"
#URL1 = "https://gist.github.com/akTwelve/c7039506130be7c0ad340e9e862b78d9/archive/73c4e1cc604aa78a45fe08dc8089515d6446f335.zip"

def get_archive(URL):
    FILE = requests.get(URL)
    open(str(os.path.dirname(__file__)) + '/archive.zip', 'wb').write(FILE.content)

#get_archive(URL1)

def file_path():
    jsons_path = []

    with ZipFile('archive.zip') as z:
        z.extractall(str(os.path.dirname(__file__)))
        for filename in z.namelist():
            jsons_path.append(str(os.path.dirname(__file__)) + '/' + str(filename))

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
                        df = df.append({'label':categories[k]['name'], 'image_name':images[i]['file_name'], 'image_width':images[i]['width'], 'image_height':images[i]['height'], 'x_min':annotations[j]['bbox'][0], 'y_min':annotations[j]['bbox'][0] , 'x_max': annotations[j]['bbox'][2] - annotations[j]['bbox'][0], 'y_max': annotations[j]['bbox'][3] - annotations[j]['bbox'][1], 'image_url':images[i]['coco_url']}, ignore_index=True)
  
    return df

def name_parse():
    names = []
    for path in file_path():
        names.append((path.split('/')[-1]).split('.')[0])
    return names

def df_to_csv(df):
    names = name_parse()
    for j in range(len(names)):
        df.to_csv(names[j] + '.csv', index=False)


jsons = open_load()

# for i in range(len(jsons)):
#     df = df_convert(jsons[i])
#     print(df)
#     df_to_csv(df)

testf = open('D:\\sample_annotations.json')
test = json.load(testf)
testf.close()
df = df_convert(test)
print(df)
df_to_csv(df)