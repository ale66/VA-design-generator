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
print(f'Got {len(input_files)} images!')


original_folder = re.sub(r"[/*?]", "-", file_selector_glob)
print("Identifier", original_folder)

#input_text = write_data_desc(input_files, input_text, use_filename=True)

def run_training(model):
    from params import *

    print('Loading arguments for training ...')

    torch_args = Args(epoch_amt, learning_rate)
    if not os.path.exists(torch_args.save_dir):
        os.makedirs(torch_args.save_dir)
    # Run training on model
    model = freeze(
        model=model,
        freeze_emb=freeze_emb,
        freeze_ln=freeze_ln,
        freeze_attn=freeze_attn,
        freeze_ff=freeze_ff,
        freeze_other=freeze_other,
    )
    print('Beginning training ...')

    # freeze params to
    train(model, input_files, torch_args, train_dataloader)

#if do_resize:
#    vae.decode = partial(slow_decode, vae)
def generate_imgs():
    from params import *

    gc.collect()
    torch.cuda.empty_cache()
    input_text = 'red shoe'
    vae = get_vae().to(device)
    model_path = os.path.join('checkpoints/lookingglass_dalle_last.pt')

    model.load_state_dict(torch.load(model_path))
    print('confidence')
    print(confidence)
    generate(vae, model, input_text, confidence = confidence, variability = variability, rurealesrgan_multiplier=rurealesrgan_multiplier, image_amount = 10)

if __name__ == '__main__':
    from train import *
    from train import model

    from vae import *
    run_training(model)
    

    generate_imgs()
