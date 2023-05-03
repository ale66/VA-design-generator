# -*- coding: utf-8 -*-
import os

import torch
from huggingface_hub import hf_hub_url, cached_download


MODELS = {
    'unet_effnetb5': dict(
        encoder_name='efficientnet-b5',
        repo_id='sberbank-ai/rudalle-Emojich',
        filename='pytorch_model_v2.bin',
        classes=2,
    ),
}


def get_emojich_unet(name, cache_dir='/tmp/rudalle'):
    assert name in MODELS
    config = MODELS[name]
    try:
        import segmentation_models_pytorch as smp
    except ImportError:
        import logging
        logging.warning('If you would like to use emojich_unet, you should reinstall timm package:'
                        '"pip install timm==0.4.12"')
        return
    model = smp.Unet(
        encoder_name=config['encoder_name'],
        encoder_weights=None,
        in_channels=3,
        classes=config['classes'],
    )
    cache_dir = os.path.join(cache_dir, name)
    filename = config['filename']
    config_file_url = hf_hub_url(repo_id=config['repo_id'], filename=f'{name}/{filename}')
    cached_download(config_file_url, cache_dir=cache_dir, force_filename=filename)
    checkpoint = torch.load(os.path.join(cache_dir, config['filename']), map_location='cpu')
    model.load_state_dict(checkpoint)
    print(f'{name} --> ready')
    return model
