
import os
import random
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
import torchvision.transforms as T
from model import *
import PIL


class RuDalleDataset(Dataset):
    clip_filter_thr = 0.24

    def __init__(
        self,
        csv_path,
        tokenizer,
        resize_ratio=0.75,
        shuffle=True,
        load_first=None,
        caption_score_thr=0.6,
    ):
        """tokenizer - object with methods tokenizer_wrapper.BaseTokenizerWrapper"""

        self.text_seq_length = model.get_param("text_seq_length")
        self.tokenizer = tokenizer
        self.target_image_size = 256
        self.image_size = 256
        self.samples = []

        self.image_transform = T.Compose(
            [
                T.Lambda(lambda img: img.convert("RGB") if img.mode != "RGB" else img),
                T.RandomResizedCrop(
                    self.image_size,
                    scale=(1.0, 1.0),  # в train было scale=(0.75., 1.),
                    ratio=(1.0, 1.0),
                ),
                T.ToTensor(),
            ]
        )

        df = pd.read_csv(csv_path)
        for caption, image_path in zip(df["caption"], df["name"]):
            if len(caption) > 10 and len(caption) < 100 and os.path.isfile(image_path):
                self.samples.append([image_path, caption])
        if shuffle:
            np.random.shuffle(self.samples)

    def __len__(self):
        return len(self.samples)

    def load_image(self, image_path):
        image = PIL.Image.open(image_path)
        return image

    def __getitem__(self, item):
        item = item % len(self.samples)  # infinite loop, modulo dataset size
        image_path, text = self.samples[item]
        try:
            image = self.load_image(image_path)
            image = self.image_transform(image).to(device)
        except Exception as err:  # noqa
            print(err)
            random_item = random.randint(0, len(self.samples) - 1)
            return self.__getitem__(random_item)
        text = (
            tokenizer.encode_text(text, text_seq_length=self.text_seq_length)
            .squeeze(0)
            .to(device)
        )
        return text, image
