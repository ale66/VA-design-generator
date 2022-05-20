### TODO ITEMS


#MODEL
Make a better parameters file so that we can control everything for training in there
Something to think about with parameters is that we may want to "overfit" to some extent in order to be more faithful to the V&A data - how can we measure this? 

Make sure it works when use_filename = False

Set up a method to do create input text in a well thought out way

Set up a different file just messing with prompts rather than re-running the model

#DATA
Collect data to use for transfer learning (compare with original model)

Create a balanced dataset of objects and styles that we might want to be able to combine

Once we have the data:
Can we create input text directly from what is in the dataset or do we need to do some preprocessing / clustering to get more discrete / defined styles?

Russian language: do we want to use a better translation service? Also: Are there any art historical terms (e.g. style names) that do not translate well into Russian? 

Style - where we don't have style data for certain objects, like shoes, how can we give it an automatic style label? For example with shoes, some makers always make shoes in a similar style e.g. all 'Rayne' shoes are labelled as 'traditional'? 

#OUTPUT 
How to judge a good match - closer or wackier? Possibility to offer multiple outputs offering a range?

It may be necessary to filter out any images with text on them - the dataset that ruDALLE was trained on has watermarks and some of the images scraped from the web, such as memes, has text (in Russian)

