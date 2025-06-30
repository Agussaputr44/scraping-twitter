import pandas as pd
import cohere
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Ganti dengan API key Anda dari Cohere
co = cohere.Client("COHERE_API_KEY")

# Nama file CSV yang berisi token dan label
filename = "data/hasil_sentimen_cohere_prompt.csv"

# Baca file CSV
df = pd.read_csv(filename)

# Pisahkan data lama (tanpa input baru untuk saat ini)
# Hapus NaN values dari texts_lama dan labels_lama
texts_lama = [str(text) if pd.notna(text) else "" for text in df['text'].tolist()]
labels_lama = [label for label in df['label'].tolist() if pd.notna(label)]

# Preprocessing dengan TF-IDF
vocab = set()
for text in texts_lama:
    if isinstance(text, str):
        vocab.update(text.split())
    else:
        print(f"Skipping invalid value: {text} (type: {type(text)})")
vectorizer = TfidfVectorizer(vocabulary=vocab, norm='l2')
tfidfnorm_lama = vectorizer.fit_transform(texts_lama).toarray()

# Fungsi untuk memprompt Cohere dan mendapatkan sentimen
def get_sentiment_with_cohere(new_text):
    new_text = str(new_text).lower()
    # Buat prompt dengan contoh dari data (hanya yang valid)
    prompt = "Berikan label sentimen ('positif' atau 'negatif') untuk teks berikut berdasarkan emosi dan konteks.\n"
    valid_texts = df['text'].dropna().head()
    valid_labels = df['label'].dropna().head()
    for ex_text, ex_label in zip(valid_texts, valid_labels):
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
        if cosine_sim[idx] > 0:  # Hanya ambil jika ada kemiripan
            print(f"{i+1}. Cosine: {cosine_sim[idx]:.4f} - Index dokumen lama: {df.index[idx]} - Label: {labels_lama[idx]}")
            labels_terdekat.append(labels_lama[idx])
        else:
            break  # Hentikan jika tidak ada kemiripan lebih lanjut

    # 5. Tentukan label baru berdasarkan mayoritas (k-NN) jika ada label terdekat
    if labels_terdekat:
        label_baru_knn = Counter(labels_terdekat).most_common(1)[0][0]
        print(f"Label dokumen baru (mayoritas dari {len(labels_terdekat)} terdekat dengan k-NN): {label_baru_knn}")
    else:
        print("Tidak ada dokumen terdekat yang cukup mirip untuk menentukan label.")

    # (Opsional) Simpan hasil
    result = pd.DataFrame({'text': [new_comment], 'label_knn': [label_baru_knn] if labels_terdekat else ['Unknown']})
    result.to_csv('data/hasil_analisis_baru.csv', mode='a', header=not pd.io.common.file_exists('data/hasil_analisis_baru.csv'), index=False)

print("Proses selesai!")