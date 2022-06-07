
# import torch
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

def run_training(model):
    from train import freeze, train, train_dataloader, Args
    print('Loading arguments for training ...')
    input_text = write_data_desc(input_files, input_text, use_filename=True)

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
    from train import model
    from vae import vae, get_vae, device, generate, generate_high_res

    #run_training(model)

    confidences = ['Medium']
    variabilities=['Ultra-High']
    gc.collect()
    torch.cuda.empty_cache()
    vae = get_vae().to(device)
    model_path = os.path.join('checkpoints/lookingglass_dalle_12000.pt')

    model.load_state_dict(torch.load(model_path))
    prompts = ['prints & drawings','vase clock']

    parameter_sweep(prompts, confidences=confidences, variabilities=variabilities)







    #low_res_img_path = 'lowres_vase_clock.png'

    #high_res = generate_high_res(low_res_img_path,rurealesrgan_multiplier,device)
    #high_res.save('highresvaseclock2.png')




''' 
checkpoint 

confidence

variability 

prompt


prompts: 
- glass shoe 
- clocks
- 1980 vase 
- vase shoe 
- clock shoe 
- vase clock 
- metal shoe
- ceramic shoe 




'''