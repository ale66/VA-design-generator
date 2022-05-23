import math
import gc
import torch
from einops import rearrange
from PIL import Image
from model import *
from datetime import datetime
import os
from rudalle import get_realesrgan
from rudalle.pipelines import (
    generate_images,
    show,
    super_resolution,
    cherry_pick_by_ruclip,
)
import numpy

try:
    from SwinIR_wrapper.SwinIR_wrapper import SwinIR_SR
except:
    try:
        import collections.abc as container_abcs
        from SwinIR_wrapper.SwinIR_wrapper import SwinIR_SR
    except:
        pass

width = 512  # @param {type:"number"}
height = 240  # @param {type:"number"}
token_width = round(width / 8)
token_height = round(height / 8)


def slow_decode(self, img_seq, token_height=round(240 / 8)):
    one_hot_indices = torch.nn.functional.one_hot(
        img_seq, num_classes=self.num_tokens
    ).float()
    z = one_hot_indices @ self.model.quantize.embed.weight
    z = rearrange(
        z,
        "b (h w) c -> b c h w",
        h=token_height
        # int(sqrt(n))
    )
    img = self.model.decode(z)
    img = (img.clamp(-1.0, 1.0) + 1) * 0.5
    return img


def aspect_crop(image_path, desired_aspect_ratio):
    """
    Return a PIL Image object cropped to desired aspect ratio
    :param str image_path: Path to the image to crop
    :param str desired_aspect_ratio: desired aspect ratio in width:height format
    """

    # compute original aspect ratio
    image = Image.open(image_path)
    width, height = image.size
    original_aspect = float(width) / float(height)

    # convert string aspect ratio into float
    w, h = map(lambda x: float(x), desired_aspect_ratio.split(":"))
    computed_aspect_ratio = w / h
    inverse_aspect_ratio = h / w

    if original_aspect < computed_aspect_ratio:
        # keep original width and change height
        new_height = math.floor(width * inverse_aspect_ratio)
        height_change = math.floor((height - new_height) / 2)
        new_image = image.crop((0, height_change, width, height - height_change))
        return new_image
    elif original_aspect > computed_aspect_ratio:
        # keep original height and change width
        new_width = math.floor(height * computed_aspect_ratio)
        width_change = math.floor((width - new_width) / 2)
        new_image = image.crop((width_change, 0, width - width_change, height))
        return new_image
    elif original_aspect == computed_aspect_ratio:
        return image


def load_params(
    input_text, prompt_text="",confidence="Ultra-Low", variability="Ultra-High"
):
    """Parameters
    Confidence is how closely the AI will attempt to match the input images.
    Higher confidence, the more the AI can go "off the rails".
    This variable is also called "top_p". Think of confidence as the "conceptual similarity" control. Default for prior versions is Low.

    #Variability affects the potential number of options that the AI can choose from for each "token", or each 8x8 chunk of pixels that it generates.
    # Higher variability, higher amount. This variable is also called "top_k". Think of variability as the "stylistic similarity" control. Default for prior versions is "High".

    """
    if confidence == "Ultra-High":
        generation_p = 0.8
    elif confidence == "High":
        generation_p = 0.9
    elif confidence == "Medium":
        generation_p = 0.99
    elif confidence == "Low":
        generation_p = 0.999
    elif confidence == "Ultra-Low":
        generation_p = 0.9999

    if variability == "Ultra-High":
        generation_k = 8192
    elif variability == "High":
        generation_k = 2048
    elif variability == "Medium":
        generation_k = 512
    elif variability == "Low":
        generation_k = 128
    elif variability == "Ultra-Low":
        generation_k = 32

    # @markdown If you'd like to prompt the AI with a different text input than what your images are captioned with, you can do so here. Leave blank to use your `input_text`. Text is automatically translated to Russian.
    if prompt_text == "":
        prompt_text = input_text
        
    input_lang = ts.language(prompt_text).result.alpha2
    if input_lang != "ru":
        prompt_text = ts.translate(input_text, "ru").result

    # Uses RealESRGAN to upscale your images at the end. That's it! Set to x1 to disable. Not recommended to be combined w/ Stretchsizing.
    rurealesrgan_multiplier = "x1"  # @param ["x1", "x2", "x4", "x8"]
    realesrgan = None
    if rurealesrgan_multiplier != "x1":
        realesrgan = get_realesrgan(rurealesrgan_multiplier, device=device)

    # @markdown Uses Swinir to upscale your images at the end. That's it! Incompatible with and overrides RealESRGan. Set to "Disabled" to disable.
    swinir_model = "Disabled"  # @param ["Disabled", "real_sr x4", "classical_sr x2", "classical_sr x3", "classical_sr x4", "classical_sr x8", "lightweight x2", "lightweight x3", "lightweight x4"]
    do_swinir = False
    if swinir_model != "Disabled":
        model_type, scale = swinir_model.split(" ")
        scale = int(scale[1])
        # initialize super resolution model
        sr = SwinIR_SR(model_type, scale)
        print(f"Loaded SWINIR {swinir_model} successfully")
        do_swinir = True
        rurealesrgan_multiplier = "x1"

    return generation_p, generation_k, prompt_text, rurealesrgan_multiplier, realesrgan


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def generate_images_amt(vae, model, images_num, generation_p, generation_k, prompt_text):
    _pil_images, _scores = generate_images(
        prompt_text,
        tokenizer,
        model,
        vae,
        top_k=generation_k,
        images_num=images_num,
        top_p=generation_p,
    )
    return _pil_images


def save_pil_images(
    pil_images,
    onlyfiles = None,
    save_output=True,
    output_filepath="output",
    original_folder="images",
):
    for k in range(len(pil_images)):
        output_name = f"lg{k}_{original_folder}.png"
        pil_images[k].save(os.path.join("output", output_name))
        if save_output:
            current_time = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
            output_name = f"{current_time}_lg{k}_{original_folder}.png"
            pil_images[k].save(os.path.join(output_filepath, output_name))

def generate(
    vae,
    model,
    confidence,
    input_text,
    image_amount = 9):
    (
        generation_p,
        generation_k,
        prompt_text,
        rurealesrgan_multiplier, #super resolution
        realesrgan, #super resolution
    ) = load_params(input_text=input_text, confidence=confidence)
    pil_images = []
    pil_images += generate_images_amt(vae, model,
        image_amount, generation_p, generation_k, prompt_text
    )

    save_pil_images(pil_images)



def show_images(
    vae,
    input_text,
    input_files,
    image_amount=9,
    collage_amount=1,
    low_mem=False,
    do_resize=False,
    do_swinir=False,
    do_stretchsize=False,
):
    (
        generation_p,
        generation_k,
        prompt_text,
        rurealesrgan_multiplier,
        realesrgan,
    ) = load_params(input_text = input_text)
    pil_images = []
    scores = []
    repeat = 1
    rows = 2
    insert = 0
    amt = 3
    skip_gt = False
    if skip_gt:
        amt = 4
    if low_mem:
        repeat = 3
        if skip_gt:
            repeat = 4
        amt = 1
    if image_amount == 9:
        repeat = 2
        rows = 3
        insert = 4
        amt = 4
        if low_mem:
            repeat = 8
            amt = 1
    elif image_amount == 25:
        repeat = 6
        rows = 5
        insert = 12
        amt = 4
        if low_mem:
            repeat = 24
            amt = 1
    elif image_amount == 1:
        repeat = 1
        rows = 1
        amt = 1
        skip_gt = True
        insert = 0

    for i in range(collage_amount):
        for j in range(repeat):
            pil_images += generate_images_amt(vae,
                amt, generation_p, generation_k, prompt_text
            )
        if skip_gt and image_amount != 4:
            if image_amount != 1:
                pil_images += generate_images_amt(1)

        onlyfiles = next(os.walk("output"))[2]
        file_to_train = random.choice(input_files)
        save_pil_images(pil_images, onlyfiles)

        if skip_gt is False:
            if do_resize:
                aspect_ratio = token_width / token_height
                with Image.open(file_to_train) as im:
                    # Provide the target width and height of the image
                    to_insert = aspect_crop(im, aspect_ratio).resize(
                        (width, height), Image.LANCZOS
                    )
            pil_images.insert(insert, to_insert.convert("RGB"))

        if do_swinir:
            for imagenum in range(len(pil_images)):
                swinir_temp = numpy.array(pil_images[imagenum])
                upsize_temp = sr.upscale(swinir_temp)
                pil_images[imagenum] = Image.fromarray(upsize_temp)
            save_pil_images(pil_images)
        if rurealesrgan_multiplier != "x1":
            pil_images = super_resolution(pil_images, realesrgan)
            save_pil_images(pil_images)

        save_collage = True
        if save_collage and image_amount != 1:
            img_width, img_height = pil_images[0].size
            collage_width = img_width * rows
            collage_height = img_height * rows
            collage = Image.new(
                "RGBA", (collage_width, collage_height), color=(255, 255, 255, 255)
            )
            c = 0
            for i in range(0, collage_width, img_width):
                for j in range(0, collage_height, img_height):
                    collage.paste(pil_images[c], (i, j))
                    c += 1
            current_time = datetime.now().strftime("%y%m%d-%H%M%S_%f")
            if do_stretchsize:
                collage = collage.resize(
                    (int(collage_width / 4), int(collage_height / 4))
                )
            else:
                collage = collage.resize((int(collage_width), int(collage_height)))
            collage.save(f"collage-{current_time}.png")
        show(pil_images, rows)

        pil_images = []
        scores = []



