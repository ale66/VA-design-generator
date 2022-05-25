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
def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    kdt_db = KDTree(rgb_values)
    _, index = kdt_db.query(rgb_tuple)
    return names[index]

def center_crop(img, frac = 0.1):
    img = Image.fromarray(img)
    left = img.size[0]*((1-frac)/2)
    upper = img.size[1]*((1-frac)/2)
    right = img.size[0]-((1-frac)/2)*img.size[0]
    bottom = img.size[1]-((1-frac)/2)*img.size[1]
    cropped_img = img.crop((left, upper, right, bottom))
    return cropped_img

def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGB")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

def get_images_by_type(object_type, save = True):
    req = requests.get(f'https://api.vam.ac.uk/v2/objects/search?q_object_type="{object_type}"')
    object_data = req.json()
    object_info = object_data["info"]
    num_pages = object_info["pages"]
    print(f"num pages={num_pages}")
    for page in range(num_pages):

        req = requests.get(
            f'https://api.vam.ac.uk/v2/objects/search?q_object_type="{object_type}"&page={page}'
        )
        object_data = req.json()
        object_records = object_data["records"]
        for i, record in enumerate(object_records):
            try:
                iiif_url = record["_images"]["_iiif_image_base_url"]
                img = iiif_image_from_url(iiif_url)
                if img.shape == (576, 768, 3):
                    cropped_img = center_crop(img)
                    # get the dominant color
                    dominant_color = get_dominant_color(cropped_img)
                    color_name = convert_rgb_to_names(dominant_color)
                    caption = (
                        f"{object_type}, "
                        + record["_currentLocation"]['displayName'].split(",")[0]
                        + f", {color_name}"
                        + ", "
                        + record["_primaryDate"]
                    )
                    if save and not os.path.exists(f"VA_data/jugs/{caption}.jpg"):
                        print(f"appending image with caption {caption} ")
                        cv2.imwrite(f"VA_data/{object_type}/{caption}.jpg", img)
            except Exception as e:
                if str(e) != "'_iiif_image_base_url'":
                    print(e)
                continue


get_images_by_type("clock", save = True)

# images = np.load('img_data.npy')
# download_jpegs(images)
