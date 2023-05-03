
# import torch
import os
from model.params import *
import re
from PIL import Image
from model.advanced_settings import *
from model.dataset import *
from utils import *
import gc

from vae import generate_high_res, generate


def run_training():

    input_files = get_input_files(file_selector_glob, do_random_crop)
    input_text = ''
    print(f'Got {len(input_files)} images!')


    original_folder = re.sub(r"[/*?]", "-", file_selector_glob)
    print("Identifier", original_folder)
    print('Loading arguments for training ...')
    #input_text = write_data_desc(input_files, input_text, use_filename=True)
    from training import freeze, train, train_dataloader, Args, model

    torch_args = Args(epoch_amt, learning_rate)
    if not os.path.exists(torch_args.save_dir):
        os.makedirs(torch_args.save_dir)
    # Run training on model
    frozen_model = freeze(
        model=model,
        freeze_emb=freeze_emb,
        freeze_ln=freeze_ln,
        freeze_attn=freeze_attn,
        freeze_ff=freeze_ff,
        freeze_other=freeze_other,
    )
    print('Beginning training ...')
    print(frozen_model)

    # freeze params to
    train(frozen_model, input_files, torch_args, train_dataloader)


def parameter_sweep(prompts, confidences, variabilities):
    for prompt in prompts:
            for confidence in confidences:
                for variability in variabilities:
                    directory_name = f'scores_10000/{prompt}'
                    if not os.path.exists(directory_name):
                        os.mkdir(directory_name)
                    print(f'generating directory: {directory_name}')
                    with torch.no_grad():
                        generate(vae, model, prompt, confidence = confidence, variability = variability, rurealesrgan_multiplier=rurealesrgan_multiplier, output_filepath=directory_name, filter_by_top = 9, image_amount = 20)


if __name__ == '__main__':

    run_training()


    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    low_res_img_path = '../../233.png'

    imgs_to_convert = 'final/'
    for low_res_img_path in os.listdir(imgs_to_convert):

        high_res = generate_high_res(f'final/{low_res_img_path}',rurealesrgan_multiplier,device)
        high_res.save(f'final/high_res_{low_res_img_path}.png')
