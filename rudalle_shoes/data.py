from netrc import NetrcParseError
import requests
from iiif_image_load import iiif_image_from_url
import numpy as np
import pickle
import cv2

def get_all_shoe_data():
    req = requests.get('https://api.vam.ac.uk/v2/objects/search?q_object_name="shoes"')
    object_data = req.json()
    object_info = object_data["info"]
    num_pages = object_info["pages"]
    all_images = []
    all_captions = []
    print(f'num pages={num_pages}')
    for page in range(num_pages):
        print(f'page={page}')

        req = requests.get(f'https://api.vam.ac.uk/v2/objects/search?q_object_name="shoes"&page={page}')
        object_data = req.json()
        object_records = object_data["records"]
        for i, record in enumerate(object_records):
            print(f'record={i}')
            try:
                iiif_url = record['_images']['_iiif_image_base_url']
                img = iiif_image_from_url(iiif_url)
                if img.shape == (576, 768, 3):
                    all_images.append(img)
                    caption = "Shoe, " + record['_primaryMaker']['name'] + ", " + record['_primaryDate']
                    print(f'appending image with caption {caption} ')
                    all_captions.append(caption)
                    cv2.imwrite(f'shoes/{caption}.jpg', img)
            except:
                print("no image data")
    all_images = np.array(all_images)
    return all_images, all_captions

def save_data(img_data, captions):
    #np.save('img_data', img_data, allow_pickle=True)
    with open("captions.txt", "wb") as fp:   #Pickling
        pickle.dump(captions, fp)

def download_jpegs(img_data, captions):
    for i, img in enumerate(img_data):
        cv2.imwrite(f'images/{captions[i]}.jpg', img)


all_images, all_captions=get_all_shoe_data()

#images = np.load('img_data.npy')
#download_jpegs(images)
