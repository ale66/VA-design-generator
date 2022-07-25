
import os
for f in os.listdir('../images-labelled'):
    if "'" in f:
        new_f = f.replace("'", '')
        os.rename(f'../images-labelled/{f}', f'../images-labelled/{new_f}')