import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import normalize
import re

input_file = "kaburajadulunormalisasi.csv"
df = pd.read_csv(input_file)

corpus = df['term'].apply(lambda x: re.sub(r'[^\w\s]', ' ', x) if isinstance(x, str) else "")
corpus = corpus.apply(lambda x: " ".join(x.split()) if x else "")

count_vectorizer_binary = CountVectorizer(binary=True, max_features=1000)
binary_matrix = count_vectorizer_binary.fit_transform(corpus).toarray()
terms_binary = count_vectorizer_binary.get_feature_names_out()
tabel_biner = pd.DataFrame(binary_matrix, index=df.index, columns=terms_binary)
tabel_biner.to_csv('tabel_biner.csv', index=False, encoding="utf-8")

count_vectorizer_row = CountVectorizer(max_features=1000)
row_matrix = count_vectorizer_row.fit_transform(corpus).toarray()
terms_row = count_vectorizer_row.get_feature_names_out()
tabel_row = pd.DataFrame(row_matrix, index=df.index, columns=terms_row)
tabel_row.to_csv('tabel_row.csv', index=False, encoding="utf-8")

row_log_matrix = np.log1p(row_matrix)
tabel_row_log = pd.DataFrame(row_log_matrix, index=df.index, columns=terms_row)
tabel_row_log.to_csv('tabel_row_log.csv', index=False, encoding="utf-8")

tfidf_vectorizer = TfidfVectorizer(lowercase=False, max_features=1000)
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus).toarray()
feature_names = tfidf_vectorizer.get_feature_names_out()
tabel_tfidf = pd.DataFrame(tfidf_matrix, index=df.index, columns=feature_names)
tabel_tfidf.to_csv('tabel_tfidf.csv', index=False, encoding="utf-8")

tfidf_normalized = normalize(tfidf_matrix, norm='l2', axis=1)
tabel_tfidf_norm = pd.DataFrame(tfidf_normalized, index=df.index, columns=feature_names)
tabel_tfidf_norm.to_csv('tabel_tfidf_norm.csv', index=False, encoding="utf-8")

print("Pembobotan selesai. File yang dihasilkan: tabel_biner.csv, tabel_row.csv, tabel_row_log.csv, tabel_tfidf.csv, tabel_tfidf_norm.csv")