from translatepy import Translator
ts = Translator()

""" Set parameters"""
file_selector_glob = "images-labelled/*"
epoch_amt = 50
do_random_crop = False


universe_similarity = (
    "Medium"  # @param ["Ultra-High","High", "Medium", "Low","Ultra-Low"]
)
# Enabling `use_filename` will cause your input text to be overwritten by the filenames of your pictures
use_filename = True
# If you'd like to change the shape or size of the output from its default 256x256 set "resize" to true. Note that this is **much slower**.
do_resize = False  # @param {type:"boolean"}

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

#Optimizer
