

from concurrent.futures import process


processed_categories = ['Education & Learning', 'Prints', 'Designs', 'Books', 
'Cameras', 'Jewellery', 'Drawings', 'Science',
 'Architectural drawings', 'Furniture', 'Christianity',
 'Transport',  'Vases', 'ELISE', 'Textiles', 'Ceramics', 'Bone China','Judaism',
  'Black History', 'Metalwork', 'Glass', 'Children & Childhood', 'Africa', 'Paintings', 'Ornament prints', 'Dolls & Toys', 
  'Boats and ships', 'Death', 'Landscapes', 'Architecture', 'Royalty', 'Animals and Wildlife', 'Wall coverings', 'Hinduism',
   'Rubbings', 'Illustration', 'Interiors', 'Fashion', 'Accessories',
   'Sculpture', 'Coins & Medals',  'Embroidery',
   'Hair and hairstyles', 'Portraits', 'Theatre', 'Islam', 'Medieval and renaissance', 'Politics', 'Caricatures & Cartoons', 'Gender and Sexuality']

category_alias_dict = {'Architectural fittings':'Architecture',
'Christianity':'Christianity (Religion)',
'Judaism':'Judaism (Religion)',
'Islam':'Islam (Religion)',
'Pattern books': 'Books',
'Hinduism': 'Hinduism (Religion)',
"Children's clothes" : 'Clothing, Fashion',
'Footwear': 'Footwear, Fashion',
'Hats & headwear': 'Hats and headwear, Fashion',
'Clothing': 'Clothing, Fashion',
'Europeana Fashion Project': 'Fashion',
'Studio Ceramics':'Ceramics',
"Men's clothes":'Clothing',
'Biblical Imagery': 'Christianity (Religion)',
'Bookbinding': 'Books',
'Mosques': 'Architecutre, Islam (Religion)'}

category_aliases = list(category_alias_dict.keys())



def process_category(category):
    if category in category_aliases:
        category = category_alias_dict[category]
        return category
    elif category in processed_categories:
        return category
    return None


processed_materials = ['paper', 'pastel', 'paint', 'card', 'pencil', 'pen and ink', 'blue ink',
'body colour', 'paper (fiber product)', 'Printing ink', 'lead glaze','porcelain',
 'rosewood', 'earthenware', 'ceramic', 'stoneware', 'glass',  'wood',
   'metal', 'bast', 'red stoneware', 'wax', 'point-paper', 'water-colour paper', 'Paper (fiber product)', 'tin glaze', 
  'jade', 'tracing vellum', 'brown paper', 'pen',
  'elephant ivory', 'Slate', 'pen and wash', 'pen and watercolour',
   'charcoal', 'manuscript paper', 'printed paper', 
   'wash','toner', 'chalk', 'coloured ink', 'drawing board', 'crayon', 'gypsum plaster',
   'charcoal black', 'plastic', 'vinyl', 'acrylic (textile)', 'textile']

material_alias_dict = {'Pencil': 'pencil','Pencil crayon':'pencil','Earthenware': 'earthenware', 'Glass':'glass', 'tin-glazed': 'tin glaze', 'copy paper': 'paper',
'water-colour':'watercolour paint',
'cotton': 'cotton fabric', 'leather':'leather fabric', 
'cotton (textile)': 'cotton textile fabric',
'machine made lace': 'machine made lace fabric',
'silk': 'silk fabric',
'oil colour':'oil colour paint',
'calf leather':'calf leather fabric',
'cardboard': 'card board',
'wool': 'wool fabric',
'Wool': 'wool fabric',
'silk (textile)': 'silk textile fabric',
'Silk (textile)':'silk textile fabric',
'Indian ink': 'ink', 
'Lithographic ink': 'ink',
'lithograhic ink': 'ink',
'roller-ball pen ink': 'ink',
'millboard': 'mill board',
'PVC':'plastic',
'Marker pen':'marker pen',
'Felt tip pen': 'pen',
'felt tip pen': 'pen',
'parian': 'porcelain, marble',
'watercolour': 'watercolour paint',
'pen and ink and watercolour': 'ink and watercolour paint',
'Pen and ink':'pen and ink',
'parchment': 'parchment paper',
'cloth':'cloth fabric',
'Parchment': 'parchment paper',
'Pastel':'pastel',
'papyrus':'papyrus paper',
'acrylic': 'acrylic paint',
'Paper': 'paper',
'bronze': 'bronze metal',
'Leather':'leather',
'Gouache':'watercolour paint',
'gouache':'watercolour paint',
'bone china': 'bone china porcelain',
'Bone china': 'bone china porcelain',
'water-base paint':'watercolour paint',
'opaque watercolour': 'watercolour paint',
 'watercolour on paper': 'watercolour paint on paper',
  'Watercolour on paper': 'watercolour paint on paper',
'vellum':'vellum paper',
 'pen and watercolour': 'pen and watercolour paint',
 'Watercolour':'watercolour',
 'Jute': 'jute (fiber product)',
 'pewter': 'metal',
 'Gold': 'gold metal',
 'gold': 'gold metal',
 'silver': 'silver metal',
 'viscose':'viscose (fiber product)',
 'brass':'brass metal',
 'Bronze': 'bronz metal',
 'muslin' : 'muslin fabric',
 'linen (material)': 'linen material fabric',
 'twill': 'twill fabric',
 'nylon': 'nylon fabric',
  'silver-gilt': 'silver gilt metal'}
material_aliases = list(material_alias_dict.keys())

def process_material(material):
    if material in material_aliases:
        material = material_alias_dict[material]
        return material
    else:
        return material

processed_techniques = ['drawn', 'print-making', 'engraving (printing process)', 'painted', 'printing', 
'letterpress', 'letterpress printing', 'painting (image-making)', 'woodcut', 
'hand painted', 'illumination', 'writing', 
'incising', 'blind stamping', 'gelatin silver process', 'turned', 'watercolour drawing', 'gilded', 'cabinet-making', 
'sand-blasting', 'engraving', 'moulding', 'glazed', 'blue and white and red', 'blue and white',
 'block printing', 'hand stitched','embroidering', 'polished', 'rubbing',
  'watercolour painting', 'hand-blown', 'inkjet printing', 'painting',
   'watercolour', 'mosaic', 
    'wood-cutting', 'wash technique', 'architectural drawing',
      'wood engraving', 'punched', 'impressed', 'gold tooling',
      'folding (process)', 'glueing', 'screen printing', 'line engraving',
       'etching (printing process)', 'engraving (printing process)', 
       'soft-ground etching', 'stipple engraving',
    'pen', 'illustration', 'laminating', 'folding', 'sketching', 'engraving (incising)', 'drawing (metal-working)',
         'impressing', 'binding', 'colour printing']

technique_alias_dict = {'mezzotint':'mezzotint printing', 'drawing':'drawn','drawing (image making)':'drawn image', 'lithography': 'lithography printing','lithograph':'lithography printing',
'chromolithography':'chromolithography printing', 'offset lithography': 'chromolithography printing', 'chromolithograph': 'chromolithography printing', 'colour lithography':'colour lithography printing','photolithography':'photolithography printing','pâte-sur-pâte': 'porcelain painting',
'inlay (process)': 'sculpture', 'encaustic decoration': 'encaustic painting','albumen process':'printing',  'embroidery':'embroidering', 'carved':'carving',
'etching':'etching (printing process)', 'drypoint': 'drypoint printing', 'writing (processes)':'writing','hand-colouring': 'hand colouring drawing','lithotint':'chromolithography print',
'calligraphy': 'calligraphy writing', 'sewing':'sewing fabric', 'stitching': 'stitching fabric', 'hand sewing': 'sewing fabric', 'aquatint':'aquatint etching','handwriting':'writing',
'free-hand drawing':'drawing','soldering':'metal working','forging': 'metal working', 'chasing': 'metal working', 'raising': 'metal working', 'carving': 'metal working stone','collage': 'collage printing', 'printed':'printing',
'digital inkjet printing':'printing','mould-melted':'metal work', 'moulded': 'metalwork', 'firing':'ceramic firing',   'xerography':'glass','copper engraving':'copper metal engraving','machine knitting':'machine knitting fabric',
'colour screen print':'colour printing', 'colour machine print': 'colour printing','transfer-printed':'printing', 'woodblock print':'wood printing','weaving':'weaving textile', 'hand weaving':'weaving textile',
'relief':'sculpting','striking':'sculpting', 'cast':'sculpting','wood-engraving (process)':'wood engraving'}

technique_aliases = list(technique_alias_dict.keys())

def process_technique(technique):
    if technique.lower() in technique_aliases:
        technique = technique_alias_dict[technique.lower()]
        return technique 
    else:
        return technique

processed_styles = ['Egyptian', 'Gothic Revival', 'Louis XIV', 'Early 20th Century', 'Victorian', 'Renaissance', 'Qing',
 'Rimpa', 'Blue and white (Asia)', 'Mughal', 'Lucknow', 'Pahari', 'Jaipur', 'Edo', 'Kalighat', 'Böttger', 'Yuan', 'STUDIO', 'Contemporary', 
 'Post Modernism', '20TH CONT', 'Arts and Crafts (movement)', 'Modernist', 'Koryô', 'Art Deco', '19th', '20th century first quarter', '1950s',
  'pre-raphaelite', 'Psychedelic']
  
def process_style(style):
    if style in processed_styles:
        return style
    return None 

england_cities = ['london','Soho (London)', 'Blackburn', 'Chesterfield', 'Chorley', 'united kingdom', 'great britain', 'Chelsea', 'Maidenhead', 'Witney', 'Covent Garden', 'Hanley', 'Stratford Upon Avon', 'Edinburgh', 'Great britain', 'Belfast', 'Nottingham', 'Newcastle upon Tyne', 'Bournemouth', 'Cardiff', 'Folkestone',
     'Coventry', 'Abingdon', 'Leeds', 'Darlington', 'Greenwich', 'Norwich', 'Stockport', 'Hatfield', 'Letchworth', 'Northern Ireland', 'Liverpool', 'Harrow', 'Blackpool', 'Dublin (city)', 'Margate',
   'Hungerford', 'Ilfracombe', 'Newport (Monmouthshire)', 'Bath', 'Derby (city)', 'Ealing', 'Nottingham (city)', 'Portsmouth (city)', 'Houston', 'Bristol (city)', 'Riddings',
  'Argenteuil', 'Leicester (city)', 'Loughborough', 'Saffron Walden', 'Great Yarmouth', 'New Barnet', 'Lincoln', 'Harrogate', 
  'Burford', 'Slough (city)', 'Huntingdon', 'Cambridge', 'Aylesbury', 'Sheffield', 'Royston', 'germany', 'Rotenburg', 'Toulouse',
   'Stratford-upon-Avon', 'Vienna (city)', 'Windsor', 'Salzburg (city)','Petworth', 'Wombwell',  'Hastings', 'Bolton', 'Manchester', 'Godalming', 'Broadstairs', 'Bradford', 'Darwen', 'Scarborough', 'Kidderminster',  'Shropshire', 'UK', 'Lambeth', 'Stoke-on-Trent', 'London','Greater London', 'Exeter', 'Suffolk', 'Birmingham', 'Edinburgh (Edinboro)', 'Chipping Campden', 'Olton', 'Essex', 
'Glasgow', 'Chelsea', 'Cardona', 'Falkirk','Oxford','Buckingham Palace', '[London]','Rochester','Chailey','Loreto','Patna', 'Clifton Junction', 'Stoke-on-Trent (city)', 'St. Helens', 'Isle of Wight','Warrington']

indian_cities = ['Tamil Nadu', 'Kolkata', 'Ludhiana','Pudukottai', 'Pune', 'Karnataka','North India','Lucknow', 'Punjab Hills', 'Jaipur','Rajasthan', 'Calcutta', 'Murshidabad', 'Ganges', 'Benares', 'Allahabad', 'Kashmir', 'Jutogh']

japanese_cities = ['Tokyo', 'Edo','Shuri','Tsutsumi']
malaysian_cities = ['Perak', 'Kuala Lumpur']

italian_cities = [ 'Naples (city)', 'Venice (city)', 'Ancona (city)', 'Florence (province)', 'italy', 'Bologna', 'Bologna (city)', 'Milan (city)', 'Northern Italy',  'Genoa', 'Urbania', 'Veneto', 'Pesaro', 'Urbino', 'Venice', 'Rome', 'Catania', 'Latium', 'Piedmont', 'Arienzo', 'Messina (Sicily)', 'Syracuse (Sicily)', 'Sicily', 
'Naples', 'Sardinia', 'Papal States', 'Parma', 'Lombardy', 'Novara', 'Florence', 'Crusinallo', 'Milano']

german_cities = ['Zwickau','Hamburg (city)', 'Berlin (city)', 'Köln (city)','Wingen-sur-Moder','Ansbach', 'Frauenau', 'Meissen','Bonn', 'Nuremberg', 'Munich', 'Cologne', 'Neuberg an der Donau', 'Saxony', 'Augsburg', 'Wesel', 'Strasbourg', 'Memmingen', 'Hamburg', 'Dresden', 'Stuttgart']

french_cities = ['Paris', 'Toulouse', 'Lille', 'Colmar', 'Lyon']

israeli_cities = ['Tel Aviv-Jaffa']

iranian_cities = ['Isfahan']

indonesian_cities = ['Sumatra']

swedish_cities = ['Stockholm', 'Lund', 'Norrköping', 'Arboga', 'Luleå', 'Göteborg', 'Piteå']

US_states = [ 'Nashville, Tennessee, USA','California','San Francisco', 'Los Angeles', 'Philadelphia', 'New York (City)','United States', 'Seattle', 'New Jersey', 'Massachussets', 'South Carolina', 'New York', 'Houston', 'Iowa']

chinese_cities = ['Shanghai', 'Hong Kong','Jingdezhen','Beijing','Mughal Empire','Mughal empire','Yixing']

turkish_cities = ['Istanbul','Constantinople']

russian_cities = ['Serbia and Montenegro','Moscow','Crimea','Sebastopol', 'Balaklava','St. Petersburg']

dutch_cities = [ 'Amsterdam','Holland', 'Innsbruck', 'Antwerp (city)', 'Zwolle', 'Sneek', 'Amsterdam', 'Leeuwarden', 'The Hague','Groningen', 'Delft']

finnish_cities = ['Nuutajärvi']

canadian_cities = ['Toronto']

danish_cities = ['Copenhagen', 'Elsinore', 'Hillerod']

spanish_cities = ['Mexico', 'Valladolid', 'Graz', 'Barcelona', 'Santiago de Compostela', 'Toledo', 'Seville', 'Valencia', 'Avila', 'Córdoba', 'Madrid','Granada']

belgium_cities = ['Luxembourg (Belgium)', 'Flanders', 'Ghent', 'Mechelen', 'Liège','Liège (province)', 'Bruges']

norwegian_cities = ['Trondheim', 'Bergen', 'Oslo']

portuguese_cities = ['Lisbon', 'Porto']

polish_cities = ['Gdansk', 'Stolp','Liegnitz',]

swiss_cities = ['Stockholm (city)', 'Zurich','[Basel]','A Geneve', 'Geneva']

latvian_cities = ['Riga']

pakistani_cities = ['Gujranwala','Sindh']
thai_cities = ['Si Satchanalai']

europe = england_cities + french_cities + spanish_cities + finnish_cities + norwegian_cities +danish_cities +swedish_cities 



country_alias_dict = {'England': 'United Kingdom', 'Britain':'United Kingdom', 'Great Britain': 'United Kingdom', 'USA': 'United States of America'}
country_aliases = list(country_alias_dict.keys())


processed_countries = ['New Zealand', 'Korea','South Africa', 'Thailand', 'Europe', 'Egypt', '[Egypt','India', 'Malaysia', 'Italy', 'United Kingdom', 'Germany', 'France', 'Israel', 'Netherlands', 'Indonesia',
 'Sweden', 'Russia', 'Denmark', 'United States of America', 'China', 'Iceland', 'Syria', 'Belgium', 'Norway', 'Spain', 'Finland', 'Canada', 'Ghana', 'Latvia',
 'Ethiopia',  'Switzerland', 'Japan', 'Portugal', 'Malta', 'Turkey', 'Poland', 'Ireland', 'Pakistan', 'Sri Lanka','Australia','Iran', 'Middle East']

all_cities = [england_cities, spanish_cities, indian_cities, malaysian_cities, italian_cities, german_cities, french_cities, israeli_cities, indonesian_cities, swedish_cities, US_states, chinese_cities, russian_cities, 
dutch_cities, finnish_cities, canadian_cities, danish_cities, belgium_cities, norwegian_cities, portuguese_cities, polish_cities, swiss_cities, latvian_cities, pakistani_cities]

city_countries = {"Egypt": [], "India": indian_cities, "Malaysia": malaysian_cities, "Italy": italian_cities, "Germany": german_cities, "United Kingdom": england_cities, "France": french_cities, "Israel": israeli_cities, "Netherlands": dutch_cities, 
"Indonesia" :indonesian_cities, "Sweden" : swedish_cities, "Russia": russian_cities, "Denmark": danish_cities, 'United States of America (USA)': US_states, "China": chinese_cities, "Iceland": [], "Syria": [], "Belgium": belgium_cities, "Norway": norwegian_cities, 
"Spain":spanish_cities, "Finland": finnish_cities, "Canada":canadian_cities, "Ghana": [], "Latvia": latvian_cities, "Ethipia": [], "Switzerland":swiss_cities, "Japan": [], "Portugal": portuguese_cities, "Malta":[], "Turkey":[], "Poland": polish_cities, "Ireland": [],
"Pakistan": pakistani_cities, "Sri Lanka": [], "Turkey":turkish_cities, "Iran":iranian_cities, "Thailand":thai_cities }

city_country_alias = {}
for k, v in city_countries.items():
    if len(v) != 0:
        for city in v:
            city_country_alias[city] = k

def process_place(place):
    if place in country_aliases:
        place = country_alias_dict[place]
    if place in processed_countries:
        return place 
    for cities in all_cities:
        if place in cities:
            place = city_country_alias[place]
            return place
    return place

def process_artist(artist):
    pass 












