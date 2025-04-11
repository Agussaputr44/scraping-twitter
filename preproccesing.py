import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk.download('punkt_tab')
nltk.download('stopwords')


input_file = "kaburajadulu.csv"
df = pd.read_csv(input_file)

stopwords_indonesia = set(stopwords.words('indonesian'))
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def process_text(text):
    
    text = str(text) if pd.notnull(text) else ""
    
    tokens = word_tokenize(text)
    
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords_indonesia]
    
    stemmed_text = stemmer.stem(text)
    
    return tokens, filtered_tokens, stemmed_text

df['tokens'], df['filtered_tokens'], df['stemmed_text'] = zip(*df['text'].apply(process_text))

df['tokens'] = df['tokens'].apply(lambda x: ', '.join(x))
df['filtered_tokens'] = df['filtered_tokens'].apply(lambda x: ', '.join(x))

output_file = "kaburajadulunormalisasi.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(df[[ 'author_id', 'created_at', 'text', 'tokens', 'filtered_tokens', 'stemmed_text']].head())