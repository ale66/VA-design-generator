import torch
import os
from params import *
import re
from PIL import Image
from advanced_settings import *
from dataset import *
from utils import *
import gc

input_files = get_input_files(file_selector_glob, do_random_crop)
input_text = ''


original_folder = re.sub(r"[/*?]", "-", file_selector_glob)
print("Identifier", original_folder)

input_text = write_data_desc(input_files, input_text, use_filename=True)

from model import *
from vae import *
def train():

    torch_args = Args(epoch_amt, learning_rate)
    if not os.path.exists(torch_args.save_dir):
        os.makedirs(torch_args.save_dir)
    # Run training on model
    model = freeze(
        model=model,
        freeze_emb=False,
        freeze_ln=False,
        freeze_attn=True,
        freeze_ff=True,
        freeze_other=False,
    )
    # freeze params to
    train(model, input_files, torch_args, train_dataloader)

#if do_resize:
#    vae.decode = partial(slow_decode, vae)
def generate_imgs():
    gc.collect()
    torch.cuda.empty_cache()

    vae = get_vae().to(device)
    model_path = os.path.join('checkpoints/lookingglass_dalle_last.pt')
   
    model.load_state_dict(torch.load(model_path))

    generate(vae, model, input_text, image_amount = 15)

if __name__ == '__main__':
    #train()
    generate_imgs()
