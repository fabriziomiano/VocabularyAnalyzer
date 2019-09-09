# Vocabulary analyzer
Are you always using the same words in
your scientific papers?
This is a tool to run a text analysis on 
PDF files containing an English corpus.

# What is it?
It's essentially the Flask WebApp of the repo [VocabularyAnalyzer](https://github.com/fabriziomiano/UzaiKeyFire),
 a simple tool to extract keywords and Part-Of-Speech distributions from a given PDF.

# How to run
Install Python3.6+, create a virtualenv and, within the environment, 

`pip install -r requirements.txt`. 

Then run 

`python runserver.py`

If all's good the local webapp will be up at [http://127.0.0.1:5000](), aka localhost.

### Considerations 
The tool is designed to run only on searchable PDF, namely PDF files
in which the text can be selected and copied. 
That's it!

# Results 
Here there are the sample results obtained by running on a PDF 
of some proceedings I wrote a long time ago, taken from [here](https://pos.sissa.it/282/856/pdf). 

#### Word cloud
![alt text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/wordcloud.png)

#### Top 20 keywords
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/kwords_count.png)

#### Top 20 nouns
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Nouns.png)

#### Top 20 adjectives
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Adjectives.png)

#### Top 20 adverbs
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Adverbs.png)

#### Top 20 verbs
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Verbs.png)

#### Top 20 entities
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Entities.png)

#### Top 20 entity types
![alt_text](https://raw.githubusercontent.com/fabriziomiano/UzaiKeyFire/master/sample/Entity%20Types.png)

## Acknowledgements
Thanks to the people at [spaCy](https://github.com/explosion/spaCy)
for the NE part, and to the guys who made 
[word cloud](https://amueller.github.io/word_cloud) for the awesome word-cloud images
that can be produced.
