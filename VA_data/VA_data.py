import requests
from iiif_image_load import iiif_image_from_url
import cv2
import webcolors 
from PIL import Image
import os
from colorthief import ColorThief 
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)
import time
import aiohttp
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd


def get_objects_by_url(url: str):
  """ This returns the object numbers of all objects that 
  are in the response of some given url"""
  try:
    vam_response = pd.read_csv(url)
  except:
    return None
  df = pd.DataFrame(vam_response)
  system_numbers = df.systemNumber
  return system_numbers

def get_image_from_obj_data(object_data):
    try:
        iiif_img = object_data['meta']['images']['_iiif_image']
        img = iiif_image_from_url(iiif_img)
        return img
    except aiohttp.ClientConnectionError:
            # something went wrong with the exception, decide on what to do next
        print("Oops, the connection was dropped before we finished")
    except aiohttp.ClientError:
        # something went wrong in general. Not a connection error, that was handled
        # above.
        print("Oops, something else went wrong with the request")
    except Exception as e:
        if str(e) != "'_iiif_image'":
            print(e)

def get_image_from_record(record):
    try:
        iiif_url = record["_images"]["_iiif_image_base_url"]
        img = iiif_image_from_url(iiif_url)
        return img

    except aiohttp.ClientConnectionError:
        # something went wrong with the exception, decide on what to do next
        print("Oops, the connection was dropped before we finished")
    except aiohttp.ClientError:
        # something went wrong in general. Not a connection error, that was handled
        # above.
        print("Oops, something else went wrong with the request")
    except Exception as e:
        if str(e) != "'_iiif_image_base_url'":
            print(e)

def get_item(name_list, record):
    if len(record) != 0:
        for i in range(len(record)):
            try:
                item = record[i]['name']['text']
            except: 
                try:
                    item = record[i]['text']
                except:
                    item = record[i]['place']['text']
            name_list.append(item)
    return name_list 

from process_data import process_category
def get_image_items(record, caption):
    image_items = {}

    artists = []
    materials = []
    techniques = []
    categories = []
    styles = []
    places = []

    description = record['briefDescription']
    description_words = description.split(' ')
    bd = ''
    for i in [0,1]:
        if description_words[i].lower() == 'cover':
            return None
        caption += f'{description[i]} ' 

    categories = get_item(categories, record['categories'])
    image_items['categories'] = categories

    if len(categories) != 0:
        processed_category = process_category(categories[0])
        if processed_category is not None:
            caption += f'{processed_category}'

    artists = get_item(artists, record['artistMakerPerson'])
    if len(artists) != 0:
        caption += f', made by {artists[0]}'
    image_items["artists"]= artists

    styles = get_item(styles, record['styles'])
    image_items['styles'] = styles
    if len(styles) != 0:
        caption += f', of style {styles[0]}'

    materials = get_item(materials, record['materials'])
    image_items["materials"] = materials
    if len(materials) != 0:
        caption += materials[0]

    techniques = get_item(techniques, record['techniques'])        
    image_items['techniques'] = techniques
    if len(techniques) != 0:
        caption += f', {techniques[0]}'
    places = get_item(places, record['placesOfOrigin'])        
    image_items['places'] = places
    if len(places) != 0:
        caption += f', from {places[0]}'

    return image_items, caption

def get_all_images():
    image_data = {}
    if not os.path.exists('data/'):
        os.mkdir('data/')

    for p in range(200):
        system_numbers = get_objects_by_url(f'https://api.vam.ac.uk/v2/objects/search/?images_exist=1&response_format=csv&page={p}&page_size=50')
        dates = []
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            #img = get_image_from_obj_data(object_data)
            #if img is None:
            #    continue

            record = object_data["record"]

            caption = ''

            image_items, caption = get_image_items(record, caption)

            if caption == '':
                continue

            image_data[obj] = image_items

    with open('saved_image_data_dict.pkl', 'wb') as f:
        pickle.dump(image_data, f)

            #with open(f'data/{p} {i}.txt', 'w') as f:
            #        f.write(caption)
            #cv2.imwrite(f"data/{p} {i}.jpg", img)
get_all_images()
# images = np.load('img_data.npy')
# download_jpegs(images)
