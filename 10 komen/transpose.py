import pandas as pd

df = pd.read_csv('data/hasil_pembobotan_normalisasi.csv', delimiter=',', index_col=0, dtype=str)

# Ubah koma menjadi titik dan konversi ke float
df = df.applymap(lambda x: float(str(x).replace(',', '.')) if x not in [None, '', ' '] else 0.0)

# Transpose data agar baris = dokumen, kolom = fitur/kata
df_T = df.transpose()

# Simpan hasil transpose ke file baru CSV
df_T.to_csv('data/data_transposed.csv')

print("Data sudah dibaca, diubah format angka, dan ditranspose.")
print(df_T.head())