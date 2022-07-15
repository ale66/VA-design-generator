import pickle 

with open('saved_image_data_dict.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

categories = []

for k,v in loaded_dict.items():
    if len(loaded_dict[k]['places']) == 0:
        continue
    if loaded_dict[k]['places'][0] not in categories:
        categories.append(loaded_dict[k]['places'][0])
print(categories)