''' Currently using Translator without a DEEPL API key but this might be something 
worth doing '''

from translatepy import Translator
ts = Translator()

""" Set file parameters"""
file_selector_glob = "images-labelled/*"

'''Number of epochs - might want to try training for longer'''
epoch_amt = 50

'''Random crop might be useful if we want to artificially get more perspectives of the object'''
do_random_crop = False

'''Universe similarity determines how close to the original images you will receive. 
Higher similarity produces images that try to stick closely to the original. 
Lower similarity produces images that use the original more as inspiration. 
**If you are getting spooky Russian AI ghosts, try turning your similarity higher or training for longer.** '''
universe_similarity = (
    "Medium"  # @param ["Ultra-High","High", "Medium", "Low","Ultra-Low"]
)

# Enabling `use_filename` will cause your input text to be overwritten by the filenames of your pictures
use_filename = True


def get_learning_rate(universe_similarity="Low"):
    if universe_similarity == "High":
        learning_rate = 1e-4
    elif universe_similarity == "Medium":
        learning_rate = 2e-5
    elif universe_similarity == "Low":
        learning_rate = 1e-5
    elif universe_similarity == "Ultra-Low":
        learning_rate = 1e-6
    elif universe_similarity == "Ultra-High":
        learning_rate = 2e-4
    return learning_rate
learning_rate = get_learning_rate(universe_similarity)

''' How many which layers we are freezing from the original model will have an affect on how our fine-tuning affects the parameters'''
freeze_emb=True
freeze_ln=False
freeze_attn=False
freeze_ff=True
freeze_other=True

''' If you'd like to change the shape or size of the output from its default 256x256 set "resize" to true. Note that this is **much slower**.'''
do_resize = False  # @param {type:"boolean"}

#@markdown Confidence is how closely the AI will attempt to match the input images. Higher confidence, the more the AI can go "off the rails". This variable is also called "top_p". Think of confidence as the "conceptual similarity" control. Default for prior versions is Low.

confidence = "Medium" #default Medium

#@markdown Variability affects the potential number of options that the AI can choose from for each "token", or each 8x8 chunk of pixels that it generates. Higher variability, higher amount. This variable is also called "top_k". Think of variability as the "stylistic similarity" control. Default for prior versions is "High".

variability = "Ultra-Low" #default Ultra-High
#Optimizer

#superresolution
rurealesrgan_multiplier = "x4"  # @param ["x1", "x2", "x4", "x8"]
