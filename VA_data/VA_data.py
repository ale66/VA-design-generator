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
    return False
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

def get_image_items(record, caption):
    image_items = {}

    artists = []
    materials = []
    techniques = []
    categories = []
    styles = []
    places = []

    caption += record['materialsAndTechniques']

    categories = get_item(categories, record['categories'])
    image_items['categories'] = categories
    caption += f', {categories[0]}'

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

    techniques = get_item(techniques, record['techniques'])        
    image_items['techniques'] = techniques

    places = get_item(places, record['placesOfOrigin'])        
    image_items['places'] = places
    if len(places) != 0:
        caption += f', from {places[0]}'

    print(caption)
    return image_items, caption

def get_images_by_category(id = None, category = None, save = True):

    image_data = {}
    for p in range(1000):
        system_numbers = get_objects_by_url(f'https://api.vam.ac.uk/v2/objects/search?id_category={id}&images_exist=1&response_format=csv&page={p}&page_size=100')
        if system_numbers == False:
            with open('saved_image_data_dict.pkl', 'wb') as f:
                pickle.dump(image_data, f)
        print(f"num object records: {len(list(system_numbers))}")
    
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue

            record = object_data["record"]
            caption = f'{p} {i} '

            image_items, caption = get_image_items(record, caption)

            image_data[obj] = image_items

            if save:

                if not os.path.exists(f"VA_data/{category}"):
                    os.mkdir(f"VA_data/{category}/")
                print(f"appending image with caption {caption} ")
                cv2.imwrite(f"VA_data/{category}/{caption}.jpg", img)

def get_all_images():
    image_data = {}
    os.mkdir('data/')

    for p in range(200):
        system_numbers = get_objects_by_url(f'https://collections.vam.ac.uk/search/?page={p}&page_size=50')

        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)
            if img is None:
                continue

            record = object_data["record"]
            caption = f'{p} {i} '

            image_items, caption = get_image_items(record, caption)

            image_data[obj] = image_items

            with open(f'data/{p} {i}.txt', 'w') as f:
                    f.write(caption)
            cv2.imwrite(f"data/{p} {i}.jpg", img)

get_all_images()
# images = np.load('img_data.npy')
# download_jpegs(images)
categories = {"ceramics": "THES48982", "porcelain": "THES48907", "textiles":"THES48885", "clothing":"THES48975", "metalwork":"THES48920",
"designs":"THES48968", "fashion":"THES48957", "SCRAN":"THES48897", "paintings":"THES48917", "ornament prints":"THES49038","drawings":"THES48966"}
