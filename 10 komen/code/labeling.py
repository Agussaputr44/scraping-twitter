import pandas as pd
import cohere

# Ganti dengan API key Anda dari Cohere
co = cohere.Client("COHERE_API_KEY")

# Ganti nama file sesuai nama file CSV kamu
filename = "token kaburajadulu.csv"

# Baca file
df = pd.read_csv(filename)

# Fungsi untuk memprompt Cohere dan mendapatkan sentimen
def get_sentiment_with_cohere(text):
    text = str(text).lower()
    # Prompt untuk meminta Cohere menganalisis sentimen
    prompt = f"Berikan label sentimen ('positif' atau 'negatif') untuk teks berikut berdasarkan emosi dan konteks: '{text}'. Hanya jawab dengan 'positif' atau 'negatif'."
    response = co.generate(
        model='command-r-plus-04-2024',  # Gunakan model yang didukung, cek dokumentasi Cohere
        prompt=prompt,
        max_tokens=10,  # Batasi panjang respons
        temperature=0.7  # Kontrol kreativitas, 0-1
    )
    # Ambil teks respons pertama
    sentiment = response.generations[0].text.strip()
    return sentiment

# Terapkan fungsi ke kolom 'token' dan simpan hasilnya
df['label'] = df['token'].apply(get_sentiment_with_cohere)

# Tampilkan hasil
print(df.head())

# Simpan ke CSV
df.to_csv('hasil_sentimen_cohere_prompt.csv', index=False)