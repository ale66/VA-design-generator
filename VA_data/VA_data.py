from netrc import NetrcParseError
import requests
from iiif_image_load import iiif_image_from_url
import numpy as np
import pickle
import cv2
import webcolors 
from PIL import Image
from matplotlib import cm

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        #r_c, g_c, b_c = int(r_c), int(g_c), int(b_c)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name

    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name

def center_crop(img):
    img = Image.fromarray(img)

    frac = 0.1

    left = img.size[0]*((1-frac)/2)
    upper = img.size[1]*((1-frac)/2)
    right = img.size[0]-((1-frac)/2)*img.size[0]
    bottom = img.size[1]-((1-frac)/2)*img.size[1]
    cropped_img = img.crop((left, upper, right, bottom))
    return cropped_img
def get_all_shoe_data(object_name, save = True):
    req = requests.get(f'https://api.vam.ac.uk/v2/objects/search?q_object_name="{object_name}"')
    print('https://api.vam.ac.uk/v2/objects/search?q_object_name="{object_name}"')
    object_data = req.json()
    object_info = object_data["info"]
    num_pages = object_info["pages"]
    all_images = []
    all_captions = []
    print(f"num pages={num_pages}")
    for page in range(num_pages):

        req = requests.get(
            f'https://api.vam.ac.uk/v2/objects/search?q_object_name="{object_name}"&page={page}'
        )
        object_data = req.json()
        object_records = object_data["records"]
        for i, record in enumerate(object_records):
            try:

                iiif_url = record["_images"]["_iiif_image_base_url"]
                img = iiif_image_from_url(iiif_url)
                if img.shape == (576, 768, 3):
                    #all_images.append(img)
                    #cropped_img = center_crop(img)
                    #average_color_row = np.max(cropped_img, axis=0)
                    #average_color = np.max(average_color_row, axis=0)
                    #named_color = closest_colour(tuple(average_color.astype(int)))
                    caption = (
                        "Jug, "
                        + record["_currentLocation"]['displayName'].split(",")[0]
                        + ", "
                        + record["_primaryDate"]
                    )
                    print(f"appending image with caption {caption} ")
                    all_captions.append(caption)
                    if save:
                        cv2.imwrite(f"VA_data/jugs/{caption}.jpg", img)
            except Exception as e:
                print(e)
                print("no image data")
    #all_images = np.array(all_images)
    #return all_images, all_captions


def save_data(img_data, captions):
    # np.save('img_data', img_data, allow_pickle=True)
    with open("captions.txt", "wb") as fp:  # Pickling
        pickle.dump(captions, fp)


def download_jpegs(img_data, captions):
    for i, img in enumerate(img_data):
        cv2.imwrite(f"jugs/{captions[i]}.jpg", img)


get_all_shoe_data("jug", save = True)

# images = np.load('img_data.npy')
# download_jpegs(images)
