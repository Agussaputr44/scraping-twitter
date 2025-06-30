import pandas as pd
import cohere
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Ganti dengan API key Anda dari Cohere
co = cohere.Client("4Va5R4AClZL45poLaxKI7IBrtXjDwjDL4alekrJ6")

# Nama file CSV yang berisi token dan label
filename = "/data/hasil_sentimen_cohere_prompt.csv"

# Baca file CSV
df = pd.read_csv(filename)

# Pisahkan data lama (tanpa input baru untuk saat ini)
texts_lama = df['token'].tolist()
labels_lama = df['label'].tolist() 

# Preprocessing dengan TF-IDF
vocab = set()  # Buat kosakata dari teks lama
for text in texts_lama:
    vocab.update(text.split())
vectorizer = TfidfVectorizer(vocabulary=vocab, norm='l2')
tfidfnorm_lama = vectorizer.fit_transform(texts_lama).toarray()

# Fungsi untuk memprompt Cohere dan mendapatkan sentimen
def get_sentiment_with_cohere(new_text):
    new_text = str(new_text).lower()
    # Buat prompt dengan contoh dari data
    prompt = "Berikan label sentimen ('positif' atau 'negatif') untuk teks berikut berdasarkan emosi dan konteks.\n"
    for ex_text, ex_label in zip(df['token'].head(), df['label'].head()):
        prompt += f"Teks: '{ex_text}' -> Label: {ex_label}\n"
    prompt += f"Teks: '{new_text}' -> Label: "

    response = co.generate(
        model='command-r-plus-04-2024',
        prompt=prompt,
        max_tokens=10,
        temperature=0.7
    )
    sentiment = response.generations[0].text.strip()
    return sentiment

# Loop untuk input data baru
while True:
    new_comment = input("Masukkan teks baru untuk analisis sentimen (atau ketik 'exit' untuk keluar): ")
    if new_comment.lower() == 'exit':
        break

    # # 1. Prediksi dengan Cohere
    # sentiment_cohere = get_sentiment_with_cohere(new_comment)
    # print(f"Sentimen dari Cohere untuk teks '{new_comment}': {sentiment_cohere}")

    # 2. Hitung TF-IDF untuk dokumen baru
    komentar_baru = [new_comment]
    tfidfnorm_baru = vectorizer.transform(komentar_baru).toarray()

    # 3. Hitung cosine similarity
    cosine_sim = cosine_similarity(tfidfnorm_baru, tfidfnorm_lama)[0]

    # 4. Temukan 5 dokumen terdekat
    top_n = 5
    sorted_idx = cosine_sim.argsort()[::-1]
    print(f"\n{top_n} Dokumen lama paling mirip (cosine):")
    labels_terdekat = []
    for i in range(top_n):
        idx = sorted_idx[i]
        print(f"{i+1}. Cosine: {cosine_sim[idx]:.4f} - Index dokumen lama: {df.index[idx]} - Label: {labels_lama[idx]}")
        labels_terdekat.append(labels_lama[idx])

    # 5. Tentukan label baru berdasarkan mayoritas (k-NN)
    label_baru_knn = Counter(labels_terdekat).most_common(1)[0][0]
    print(f"Label dokumen baru (mayoritas dari {top_n} terdekat dengan k-NN): {label_baru_knn}")

    # (Opsional) Simpan hasil
    result = pd.DataFrame({'text': [new_comment], 'label_knn': [label_baru_knn]})
    result.to_csv('/data/hasil_analisis_baru.csv', mode='a', header=not pd.io.common.file_exists('/data/hasil_analisis_baru.csv'), index=False)

print("Proses selesai!")