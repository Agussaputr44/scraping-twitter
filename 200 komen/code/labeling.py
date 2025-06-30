import pandas as pd
import cohere
import time

co = cohere.Client("COHERE_API_KEY")

filename = "data/kaburajadulunormalisasi.csv"

try:
    # Baca file
    df = pd.read_csv(filename)
    print(f"File {filename} berhasil dibaca.")

    # Fungsi untuk memprompt Cohere dan mendapatkan sentimen
    def get_sentiment_with_cohere(text):
        text = str(text).lower()
        prompt = f"Berikan label sentimen ('positif' atau 'negatif') untuk teks berikut berdasarkan emosi dan konteks: '{text}'. Hanya jawab dengan 'positif' atau 'negatif'."
        response = co.generate(
            model='command-r-plus-04-2024',
            prompt=prompt,
            max_tokens=10,
            temperature=0.7
        )
        sentiment = response.generations[0].text.strip()
        return sentiment

    # Proses dalam batch untuk menghindari batas API
    batch_size = 20
    for i in range(0, len(df), batch_size):
        batch = df['text'].iloc[i:i + batch_size]
        df.loc[i:i + batch_size - 1, 'label'] = batch.apply(get_sentiment_with_cohere)
        print(f"Memproses batch {i//batch_size + 1}...")
        time.sleep(40) 

    # Tampilkan hasil
    print(df.head())

    # Simpan ke CSV
    df.to_csv('data/hasil_sentimen_cohere_prompt.csv', index=False)
    print("Hasil telah disimpan ke 'hasil_sentimen_cohere_prompt.csv'.")

except FileNotFoundError:
    print(f"Error: File '{filename}' tidak ditemukan. Pastikan file ada di direktori 'data' atau perbarui path.")
except Exception as e:
    print(f"Terjadi error: {e}")