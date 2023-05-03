from regex import F
import requests
from iiif_image_load import iiif_image_from_url
import cv2
from PIL import Image
import aiohttp
import matplotlib.pyplot as plt
import pickle
import pandas as pd


def get_objects_by_url(url: str):
  """ This returns the object numbers of all objects that 
  are in the response of some given url"""
  try:
    vam_response = pd.read_csv(url)
  except:
    return None
  df = pd.DataFrame(vam_response)
  system_numbers = df.systemNumber
  return system_numbers

def get_image_from_obj_data(object_data):
    try:
        iiif_img = object_data['meta']['images']['_iiif_image']
        img = iiif_image_from_url(iiif_img)
        return img
    except aiohttp.ClientConnectionError:
            # something went wrong with the exception, decide on what to do next
        print("Oops, the connection was dropped before we finished")
    except aiohttp.ClientError:
        # something went wrong in general. Not a connection error, that was handled
        # above.
        print("Oops, something else went wrong with the request")
    except Exception as e:
        if str(e) != "'_iiif_image'":
            print(e)

def get_image_from_record(record):
    try:
        iiif_url = record["_images"]["_iiif_image_base_url"]
        img = iiif_image_from_url(iiif_url)
        return img

    except aiohttp.ClientConnectionError:
        # something went wrong with the exception, decide on what to do next
        print("Oops, the connection was dropped before we finished")
    except aiohttp.ClientError:
        # something went wrong in general. Not a connection error, that was handled
        # above.
        print("Oops, something else went wrong with the request")
    except Exception as e:
        if str(e) != "'_iiif_image_base_url'":
            print(e)

def get_item(name_list, record):
    if len(record) != 0:
        for i in range(len(record)):
            try:
                item = record[i]['name']['text']
            except: 
                try:
                    item = record[i]['text']
                except:
                    item = record[i]['place']['text']
            name_list.append(item)
    return name_list 

from process_data import process_category, process_technique, process_material, process_place
def get_image_items(record, caption):
    image_items = {}

   # artists = []
    materials = []
    techniques = []
    categories = []
    styles = []
    places = []

    description = record['briefDescription']
    description_words = description.split(' ')
    if len(description_words) > 5:
        for i in [0,4]:
            caption += f'{description_words[i]} ' 
    else:
        caption += description

    categories = get_item(categories, record['categories'])

    image_items['categories'] = categories

    if len(categories) != 0:
        processed_category = process_category(categories[0])
        if processed_category is None:
            return None, None
        caption += f' {processed_category}'

   # artists = get_item(artists, record['artistMakerPerson'])
   # if len(artists) != 0:
   #     caption += f', made by {artists[0]}'
   # image_items["artists"]= artists

    styles = get_item(styles, record['styles'])
    image_items['styles'] = styles
    if len(styles) != 0:
        caption += f', of style {styles[0]}'

    materials = get_item(materials, record['materials'])
    image_items["materials"] = materials
    if len(materials) != 0:
        material = process_material(materials[0])
        caption += f' {material} '

    techniques = get_item(techniques, record['techniques'])        
    image_items['techniques'] = techniques
    if len(techniques) != 0:
        technique = process_technique(techniques[0])
        caption += f', {technique} '
   
   
    places = get_item(places, record['placesOfOrigin'])        
    image_items['places'] = places
    if len(places) != 0:
        place = process_place(places[0])
        caption += f', from {place}'

    return image_items, caption
'''
def get_all_images():
    image_data = {}
    if not os.path.exists('data/'):
        os.mkdir('data/')

    for p in range(200):
        system_numbers = get_objects_by_url(f'https://api.vam.ac.uk/v2/objects/search/?images_exist=1&response_format=csv&page={p}&page_size=50')
        dates = []
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)
            if img is None:
                continue

            record = object_data["record"]

            caption = ''

            image_items, caption = get_image_items(record, caption)
            if image_items is None:
                continue

            if caption == '':
                continue

            image_data[obj] = image_items

    with open('saved_image_data_dict.pkl', 'wb') as f:
        pickle.dump(image_data, f)
'''
            #with open(f'data/{p} {i}.txt', 'w') as f:
            #        f.write(caption)
            #cv2.imwrite(f"data/{p} {i}.jpg", img)

def get_images_by_category(id, category):
    print(category)

    image_data = {}
    for p in range(1000000):
        try:
            system_numbers = get_objects_by_url(f'https://api.vam.ac.uk/v2/objects/search?id_category={id}&images_exist=1&response_format=csv&page={p}&page_size=100')
            print(f"num object records: {len(list(system_numbers))}")
        
        except:
            with open(f'saved_image_data_dict_{category}.pkl', 'wb') as f:
                pickle.dump(image_data, f)    
            break
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            caption = ''
            record = object_data["record"]
            image_items, caption = get_image_items(record, caption)
            if image_items is None:
                continue
            image_data[obj] = image_items
            print(caption)


            with open(f'data/{category} {p} {i}.txt', 'w') as f:
                    f.write(caption)
            cv2.imwrite(f"data/{category} {p} {i}.jpg", img)


#'THES48982':'Ceramics',
categories = { 'THES48907':'Porcelain','THES48957':'Fashion', 'THES48975':'Clothing',
'THES49044':'Womens clothes', 'THES48920':'Metalwork', 'THES4890':'Jewellery', 'THES48885':'Textiles'}

#for k, v in categories.items():
#    get_images_by_category(k,v)
# images = np.load('img_data.npy')
# download_jpegs(images)


ceramics_rie_lucie = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A2766&images_exist=1&response_format=csv'

ceramics_johann_kandler = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A6734&images_exist=1&response_format=csv'

ceramics_hunt_martin = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A1256&images_exist=1&response_format=csv'

ceramics_robert_hancock = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A8473&images_exist=1&response_format=csv'

ceramics_stanley_lane = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=AUTH348934&images_exist=1&response_format=csv'

ceramics_green_guy = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A3058&images_exist=1&response_format=csv'

ceramics_keith_murray = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A818&images_exist=1&response_format=csv'

ceramics_william_de_morgan = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A8328&images_exist=1&response_format=csv'

ceramics_tapio_wirkkala = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=THES48594&images_exist=1&response_format=csv'

ceramics_susie_cooper = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48594&id_person=A1490&images_exist=1&response_format=csv'

URLS = [ceramics_rie_lucie, ceramics_johann_kandler, ceramics_hunt_martin, ceramics_robert_hancock, ceramics_stanley_lane, ceramics_green_guy, 
ceramics_keith_murray, ceramics_william_de_morgan, ceramics_tapio_wirkkala, ceramics_susie_cooper]

URLS = [f'https://api.vam.ac.uk/v2/objects/search?q=wedgwood&id_organisation=A1450&images_exist=1&response_format=csv'
]
def get_item_2(record):
    if len(record) != 0:
        for i in range(len(record)):
            try:
                item = record[i]['name']['text']
            except: 
                try:
                    item = record[i]['text']
                except:
                    item = record[i]['place']['text']
        return item
    return []


furniture_rococo = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=AAT21155&images_exist=1&response_format=csv'
furniture_neoclassical = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=x38958&images_exist=1&response_format=csv'

furniture_baroque = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=AAT21147&images_exist=1&response_format=csv'
furniture_art_deco = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=AAT21426&images_exist=1&response_format=csv'
furniture_art_nouveau = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=AAT21430&images_exist=1&response_format=csv'

furniture_post_modernist = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48597&id_style=AAT22208&images_exist=1&response_format=csv'

furniture_chinese = f'https://api.vam.ac.uk/v2/objects/search?id_category=THES48948&id_place=x29398&images_exist=1&response_format=csv'

URLS = [furniture_rococo, furniture_neoclassical, furniture_baroque, furniture_art_deco, furniture_art_nouveau, furniture_post_modernist, furniture_chinese]

fashion_balenciaga = f'https://api.vam.ac.uk/v2/objects/search/?id_collection=THES48602&id_category=THES269529&images_exist=1&response_format=csv'


URLS = [fashion_balenciaga]
for j, f in enumerate(URLS):
    for p in range(100):
        try:
            system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')
            print(f"num object records: {len(list(system_numbers))}")
        
        except:
            break
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            if j == 0:
                caption = 'Fashion, Theatrical'
            elif j == 1:
                caption = 'Furniture, Neoclassical'
            elif j == 2:
                caption = 'Furniture, Baroque'
            elif j == 3:
                caption = 'Furniture, Art Deco'
            elif j == 4:
                caption = 'Furniture, Art Nouveau'
            elif j == 5:
                caption == 'Furniture, Post Modernist'
            elif j == 6:
                caption == 'Furniture, Chinese'
            record = object_data["record"]



            description = record['briefDescription']
            description_words = description.split(' ')
            if len(description_words) > 3:
                for i in range(2):
                    caption += f', {description_words[i]} ' 
            else:
                caption += f', {description}'

            styles = get_item_2(record['styles'])
            if len(styles) != 0:
                caption += f', of style {styles}'

            materials = get_item_2(record['materials'])
            if len(materials) != 0:
                material = process_material(materials)
                caption += f' made of {material} '

            techniques = get_item_2(record['techniques'])        
            if len(techniques) != 0:
                technique = process_technique(techniques)
                caption += f', with technique {technique} '
        
        
            cv2.imwrite(f"images-labelled/fashion/{caption}.jpg", img)

""" 


paintings_raphael = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A5306&images_exist=1&response_format=csv'

paintings_redgrave = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A8777&images_exist=1&response_format=csv'

paintings_peter_duwint = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A2112&images_exist=1&response_format=csv'

paintings_joseph_turner = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A8934&images_exist=1&response_format=csv'

paintings_rowntree_kenneth = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A23684&images_exist=1&response_format=csv'

paintings_rownlandson = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A2367&images_exist=1&response_format=csv'

paintings_vincent_henry = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A34471&images_exist=1&response_format=csv'

paintings_carlevarijs = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A18624&images_exist=1&response_format=csv'

paintings_kaiser = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48595&id_category=THES48917&id_person=A15980&images_exist=1&response_format=csv'

URLS = [paintings_raphael, paintings_redgrave, paintings_peter_duwint, paintings_joseph_turner, paintings_rowntree_kenneth, paintings_rownlandson, 
paintings_vincent_henry, paintings_carlevarijs, paintings_kaiser]


for j, f in enumerate(URLS):
    for p in range(100):
        try:
            system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')
            print(f"num object records: {len(list(system_numbers))}")
        
        except:
            break
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            if j == 0:
                caption = 'Paintings, by Raphael'
            elif j == 1:
                caption = 'Paintings, by Redgrave'
            elif j == 2:
                caption = 'Paintings, by Peter Duwint'
            elif j == 3:
                caption = 'Paintings, by Joseph Turner'
            elif j == 4:
                caption = 'Paintings by Kenneth Rowntree'
            elif j == 5:
                caption == 'Paintings, by Rowlandson'
            elif j == 6:
                caption = 'Paintings, by Henry Vincent'
            elif j == 7:
                caption = 'Paintings, by Luca Carlevarijs'
            elif j == 8:
                caption = 'Paintings, by Kaiser'

            record = object_data["record"]



            description = record['briefDescription']
            description_words = description.split(' ')
            if len(description_words) > 3:
                for i in range(2):
                    caption += f', {description_words[i]} ' 
            else:
                caption += f', {description}'

            styles = get_item_2(record['styles'])
            if len(styles) != 0:
                caption += f', of style {styles}'

            materials = get_item_2(record['materials'])
            if len(materials) != 0:
                material = process_material(materials)
                caption += f' made of {material} '

            techniques = get_item_2(record['techniques'])        
            if len(techniques) != 0:
                technique = process_technique(techniques)
                caption += f', with technique {technique} '
        
        
            cv2.imwrite(f"images-labelled/paintings/{caption} {p} {i}.jpg", img)

"""


fashion_lucienne_day = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A2110&images_exist=1&response_format=csv'

fashion_eveline_gordon = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A10092&images_exist=1&response_format=csv'

fashion_william_morris = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A8676&images_exist=1&response_format=csv'

fashion_yves_saint_laurent = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A2540&images_exist=1&response_format=csv'

fashion_vivienne_westwood = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A4913&images_exist=1&response_format=csv'

fashion_balenciaga = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A2011&images_exist=1&response_format=csv'

fashion_versace = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A6328&images_exist=1&response_format=csv'

fashion_frank_willis = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=N11788&images_exist=1&response_format=csv'

fashion_barbara_brown = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A2949&images_exist=1&response_format=csv'

fashion_barbara_brown = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48601&id_person=A2949&images_exist=1&response_format=csv'

URLS = [fashion_lucienne_day, fashion_eveline_gordon, fashion_william_morris, fashion_yves_saint_laurent, fashion_balenciaga, fashion_balenciaga, 
fashion_versace, fashion_frank_willis,fashion_barbara_brown]

fashion_yoruba = f'https://api.vam.ac.uk/v2/objects/search?q=yoruba&id_category=THES48885&images_exist=1&response_format=csv'

URLS = [fashion_yoruba]
for j, f in enumerate(URLS):
    for p in range(100):
        try:
            system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')
            print(f"num object records: {len(list(system_numbers))}")
        
        except:
            break
        for i, obj in enumerate(system_numbers):

            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()
            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            if j == 0:
                caption = 'Textiles, by Yoruba women'
            elif j == 1:
                caption = 'Fashion, by Eveline Gordon'
            elif j == 2:
                caption = 'Fashion, by William Morris'
            elif j == 3:
                caption = 'Fashion, by Yves Saint Laurent'
            elif j == 4:
                caption = 'Fashion, by Vivienne Westwood'
            elif j == 5:
                caption == 'Fashion, by Balenciaga'
            elif j == 6:
                caption = 'Fashion, by Versace'
            elif j == 7:
                caption = 'Fashion, by Frank Willis'
            elif j == 8:
                caption = 'Fashion, by Barbara Brown'

            record = object_data["record"]



            description = record['briefDescription']
            description_words = description.split(' ')
            if len(description_words) > 3:
                for i in range(2):
                    caption += f', {description_words[i]} ' 
            else:
                caption += f', {description}'

            styles = get_item_2(record['styles'])
            if len(styles) != 0:
                caption += f', of style {styles}'

            materials = get_item_2(record['materials'])
            if len(materials) != 0:
                material = process_material(materials)
                caption += f' made of {material} '

            techniques = get_item_2(record['techniques'])        
            if len(techniques) != 0:
                technique = process_technique(techniques)
                caption += f', with technique {technique} '
        
        
            cv2.imwrite(f"images-labelled/fashion/{caption} {p} {i}.jpg", img)

raise

east_asia_utagawa_kunisada = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A3234&images_exist=1&response_format=csv'

east_asia_keisai_eisein = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A6849&images_exist=1&response_format=csv'

east_asia_utagawa_hiroshige = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A2428&images_exist=1&response_format=csv'

east_asia_yamamotoya_heikichi = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A3379&images_exist=1&response_format=csv'

east_asia_utagawa_kuniyoshi = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A6818&images_exist=1&response_format=csv'

east_asia_katsushika_hokusai = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A6847&images_exist=1&response_format=csv'

east_asia_minatoya_kohei = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=A3326&images_exist=1&response_format=csv'

east_asia_chiang_yee = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=AUTH326015&images_exist=1&response_format=csv'
east_asia_wang_gai = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48596&id_person=AUTH349397&images_exist=1&response_format=csv'


URLS = [east_asia_utagawa_kunisada, east_asia_keisai_eisein, east_asia_utagawa_hiroshige, east_asia_yamamotoya_heikichi, east_asia_utagawa_kuniyoshi, 
east_asia_katsushika_hokusai, east_asia_minatoya_kohei, east_asia_chiang_yee, east_asia_wang_gai]


for j, f in enumerate(URLS):
    for p in range(100):
        try:
            system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')

        except:
            break
        for i, obj in enumerate(system_numbers):
            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')

            object_data = req.json()

            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()

            if j == 0:
                caption = 'East Asia, by Utagawa Kunisada'
            elif j == 1:
                caption = 'East Asia, by Keisai Eisein'
            elif j == 2:
                caption = 'East Asia, by Utagawa Hiroshige'
            elif j == 3:
                caption = 'East Asia, by Yamamotoya Heikichi'
            elif j == 4:
                caption = 'East Asia, by Utagawa Kuniyoshi'
            elif j == 5:
                caption == 'East Asia, by Katsushika Hokusai'
            elif j == 6:
                caption = 'East Asia, by Minatoya Kohei'
            elif j == 7:
                caption = 'East Asia, by Chiang Yee'
            elif j == 8:
                caption = 'East Asia, by Wang Gai'

            record = object_data["record"]



            description = record['briefDescription']
            description_words = description.split(' ')
            if len(description_words) > 3:
                for i in range(2):
                    caption += f', {description_words[i]} ' 
            else:
                caption += f', {description}'

            styles = get_item_2(record['styles'])
            if len(styles) != 0:
                caption += f', of style {styles}'

            materials = get_item_2(record['materials'])
            if len(materials) != 0:
                material = process_material(materials)
                caption += f' made of {material} '

            techniques = get_item_2(record['techniques'])        
            if len(techniques) != 0:
                technique = process_technique(techniques)
                caption += f', with technique {technique} '
        
        
            cv2.imwrite(f"images-labelled/east_asia/{caption} {p} {i}.jpg", img)


metalwork_paul_storr = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8891&images_exist=1&response_format=csv'

metalwork_paul_lamerie = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8591&images_exist=1&response_format=csv'

metalwork_hester_bateman = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A10629&images_exist=1&response_format=csv'

metalwork_garrard_robert = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8414&images_exist=1&response_format=csv'

metalwork_ashbee_robert = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8102&images_exist=1&response_format=csv'

metalwork_archibald_knox = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8584&images_exist=1&response_format=csv'

metalwork_joseph_wilmmore = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A10143&images_exist=1&response_format=csv'

metalwork_phillip_rollos = f'https://api.vam.ac.uk/v2/objects/search?id_collection=THES48599&id_person=A8796&images_exist=1&response_format=csv'

URLS =[metalwork_paul_lamerie, metalwork_hester_bateman, metalwork_garrard_robert, metalwork_ashbee_robert,
metalwork_archibald_knox, metalwork_joseph_wilmmore, metalwork_phillip_rollos]

for j, f in enumerate(URLS):
    for p in range(100):
        try:
            system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')
            print(f"num object records: {len(list(system_numbers))}")
        
        except:
            break
        for i, obj in enumerate(system_numbers):
            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')

            object_data = req.json()

            img = get_image_from_obj_data(object_data)            
            if img is None:
                continue
            req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
            object_data = req.json()

            if j == 0:
                caption = 'Metalwork, by Paul Storr'
            elif j == 1:
                caption = 'Metalwork, by Paul Lamerie'
            elif j == 2:
                caption = 'Metalwork, by Hester Bateman'
            elif j == 3:
                caption = 'Metalwork, by Garrard Robert'
            elif j == 4:
                caption = 'Metalwork, by Ashbee Robert'
            elif j == 5:
                caption == 'Metalwork, by Archibald Knox'
            elif j == 6:
                caption = 'Metalwork, by Joseph Wilmore'
            elif j == 7:
                caption = 'Metalwork, by Phillip Rollos'


            record = object_data["record"]



            description = record['briefDescription']
            description_words = description.split(' ')
            if len(description_words) > 3:
                for i in range(2):
                    caption += f', {description_words[i]} ' 
            else:
                caption += f', {description}'

            styles = get_item_2(record['styles'])
            if len(styles) != 0:
                caption += f', of style {styles}'

            materials = get_item_2(record['materials'])
            if len(materials) != 0:
                material = process_material(materials)
                caption += f' made of {material} '

            techniques = get_item_2(record['techniques'])        
            if len(techniques) != 0:
                technique = process_technique(techniques)
                caption += f', with technique {technique} '
        
        
            cv2.imwrite(f"images-labelled/metalwork/{caption} {p} {i}.jpg", img)
# for j, f in enumerate(URLS):
#     for p in range(100):
#         try:
#             system_numbers = get_objects_by_url(f'{f}&page={p}&page_size=100')
#             print(f"num object records: {len(list(system_numbers))}")
        
#         except:
#             break
#         for i, obj in enumerate(system_numbers):

#             req = requests.get(f'https://api.vam.ac.uk/v2/museumobject/{obj}')
#             object_data = req.json()
#             img = get_image_from_obj_data(object_data)            
#             if img is None:
#                 continue
#             if j == 0:
#                 caption = 'Ceramics, by Rie Lucie'
#             elif j == 1:
#                 caption = 'Ceramics, by Johann Kandler'
#             elif j == 2:
#                 caption = 'Ceramics, by Hunt Martin'
#             elif j == 3:
#                 caption = 'Ceramics, by Robert Hancock'
#             elif j == 4:
#                 caption = 'Ceramics, by Stanley Lane'
#             elif j == 5:
#                 caption == 'Ceramics, by Guy Green'
#             elif j == 6:
#                 caption = 'Ceramics, by Keith Murray'
#             elif j == 7:
#                 caption = 'Ceramics, by William de Morgan'
#             elif j == 8:
#                 caption = 'Ceramics, by Tapio Wirkkala'
#             elif j == 9:
#                 caption = 'Ceramics, by Susie Cooper'
#             record = object_data["record"]



#             description = record['briefDescription']
#             description_words = description.split(' ')
#             if len(description_words) > 3:
#                 for i in range(2):
#                     caption += f', {description_words[i]} ' 
#             else:
#                 caption += f', {description}'

#             styles = get_item_2(record['styles'])
#             if len(styles) != 0:
#                 caption += f', of style {styles}'

#             materials = get_item_2(record['materials'])
#             if len(materials) != 0:
#                 material = process_material(materials)
#                 caption += f' made of {material} '

#             techniques = get_item_2(record['techniques'])        
#             if len(techniques) != 0:
#                 technique = process_technique(techniques)
#                 caption += f', with technique {technique} '
        
        
#             cv2.imwrite(f"images-labelled/ceramics/{caption} {p} {i}.jpg", img)