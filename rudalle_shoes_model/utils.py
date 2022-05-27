from PIL import Image
import glob
from pathlib import Path
from advanced_settings import random_crop
from deep_translator import DeepL as DeeplTranslator 
from translatepy import Translator
ts = Translator()
import csv

random_crop_size = 240
num_crops = 24

def get_input_files(file_selector_glob, do_random_crop=False):
    input_files = glob.glob(file_selector_glob, recursive=True)
    for i in input_files:
        if "_" in i:
            raise ValueError(
                "Please remove all underscores (the _ character) from your files before proceeding!"
            )
        if "'" in i:
            raise ValueError(
                "Please remove all apostrophes (the ' character) from your files before proceeding!"
            )

    if len(input_files) == 0:
        print(
            "Your input files are empty! This will error out - make sure your file_selector_glob is formatted correctly!"
        )

    if do_random_crop:
        Path("/content/crops").mkdir(parents=True, exist_ok=True)
        for image_path in input_files:
            image = Image.open(image_path)
            if image.size[0] > random_crop_size and image.size[1] > random_crop_size:
                # math.floor((image.size[0]*image.size[1])/(rcrop_size*rcrop_size))
                random_crop(image_path, random_crop_size, num_crops, "/content/crops")

    return input_files


def set_input_text(input_text="", deepl_api_key=""):
    """If you have a DeepL API key, you can insert it here to use DeepL translation for the auto-translator, which generally produces better results. Otherwise, the default auto-translator is used."""
    if input_text != "":
        if len(input_text) < 10:
            raise ValueError("Your input text is too short. Please make it longer!")
        if len(input_text) > 100:
            raise ValueError("Your input text is too long. Please make it shorter!")
    elif input_text == "":
        input_text = "\u0420\u0438\u0447\u0430\u0440\u0434 \u0414. \u0414\u0436\u0435\u0439\u043C\u0441"
    else:
        input_lang = ts.language(input_text).result.alpha2
        if input_lang != "ru":
            if deepl_api_key != "":
                input_text = DeeplTranslator(
                    api_key=deepl_api_key,
                    source=input_lang,
                    target="ru",
                    use_free_api=True,
                ).translate(input_text)
            else:
                input_text = ts.translate(input_text, "ru").result
    return input_text


def write_data_desc(input_files, input_text="", use_filename=True, deepl_api_key=""):

    with open("data_desc.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(["", "name", "caption"])
        for i, filepath in enumerate(input_files):
            text = ""
            if use_filename:
                filename = Path(filepath).stem
                input_lang = ts.language(filename).result.alpha2
                text = ts.translate(filename, "ru").result
            else:
                text = input_text
            csvwriter.writerow([i, filepath, text])

    print(f'Wrote {len(input_files)} lines to the data_desc file')
    return text
