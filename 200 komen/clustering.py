import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


tabel_tfidf_norm = pd.read_csv('tabel_tfidf_norm.csv', encoding="utf-8")

n_clusters = 2  
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, random_state=42, verbose=0)
kmeans.fit(tabel_tfidf_norm)

df = pd.read_csv("kaburajadulunormalisasi.csv")  
df['cluster'] = kmeans.labels_

output_file = "kaburajadulu_kmeans.csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Hasil K-Means disimpan ke {output_file}")

print("\nHasil K-Means (5 baris pertama):")
print(df[['author_id', 'created_at', 'text', 'cluster']].head())

print("\nJumlah dokumen per klaster:")
print(df['cluster'].value_counts())

print("\nCentroid akhir (5 fitur pertama):")
feature_names = tabel_tfidf_norm.columns  
print(pd.DataFrame(kmeans.cluster_centers_, columns=feature_names).iloc[:, :5])

print(f"\nJumlah iterasi yang dilakukan: {kmeans.n_iter_}")

pca = PCA(n_components=2)
reduced_data = pca.fit_transform(tabel_tfidf_norm)

plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=kmeans.labels_, cmap='viridis')
plt.title('Visualisasi Klaster Laporan')
plt.xlabel('Komponen PCA 1')
plt.ylabel('Komponen PCA 2')
plt.savefig('cluster_visualization.png')
plt.show()