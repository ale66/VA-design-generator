import random
import math
from PIL import Image


def all_crops(image_path, distance_between_crops, out_path):
    """
    Saves all square-sized crops starting from the leftmost or topmost edge of the image.
    :param str image_path: Path to the image to crop
    :param int distance_between_crops: Distance between each unique crop in pixels
    :param str out_path: Directory to save images
    """

    image_name = image_path.split("/")[-1].split(".")[0]
    image = Image.open(image_path)

    # calculate valid center points
    width, height = image.size
    size = 256
    center_width = 0
    center_height = 0
    num_crops = 1
    horizontal = True
    if width > height:
        center_width = center_height = int(height / 2)
        size = height
        num_crops = int(round((width - height) / distance_between_crops)) + 1
    elif height >= width:
        center_width = center_height = int(width / 2)
        size = width
        num_crops = int(round((height - width) / distance_between_crops)) + 1
        horizontal = False
    s2 = int(round(size / 2))

    for _ in range(num_crops):
        image.crop(
            (
                center_width - s2,
                center_height - s2,
                center_width + s2,
                center_height + s2,
            )
        ).save(
            f"{out_path}/{image_name}-cropped-{size}px-{center_width}-{center_height}.png"
        )
        if horizontal:
            center_width = center_width + distance_between_crops
        else:
            center_height = center_height + distance_between_crops
    print(str(num_crops) + " images generated line crop")


def random_crop(image_path, size, num_crops, out_path):
    """
    Save images cropped to desired size with random center points
    Only valid unique crops are saved, even if its fewer than num_crops
    :param str image_path: Path to the image to crop
    :param int size: Size in pixels of desired crop
    :param int num_crops: Number of crops desired
    :param str out_path: Directory to save images
    """

    image_name = image_path.split("/")[-1].split(".")[0]
    image = Image.open(image_path)

    if size % 2 != 0:
        raise Exception("crop size must be even")
    if any(map(lambda x: x < size + 1, image.size)):
        raise Exception(
            f"image size of:{image.size} too small for crop size of: {size}"
        )

    # calculate valid center points
    width, height = image.size
    left_bound, top_bound = size / 2, size / 2
    right_bound = width - size / 2
    bottom_bound = height - size / 2
    valid_center_points = int((right_bound - left_bound) * (bottom_bound - top_bound))

    # if there are fewer valid center points than requested crops
    # then produce fewer crops
    if valid_center_points < num_crops:
        num_crops = valid_center_points

    used_center_points = []
    for _ in range(num_crops):
        # ensure uniqueness of center points
        # slower when valid_center_points is near num_crops
        while True:
            w = random.randrange(left_bound, right_bound)
            h = random.randrange(top_bound, bottom_bound)
            if not ([w, h] in used_center_points):
                break

        used_center_points.append([w, h])

        image.crop(
            (w - (size / 2), h - (size / 2), w + (size / 2), h + (size / 2))
        ).save(f"{out_path}/{image_name}-cropped-{size}px-{w}-{h}.png")
    print(str(num_crops) + " images generated random crop")
