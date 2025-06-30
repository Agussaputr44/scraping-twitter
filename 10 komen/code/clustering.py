import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

df_data = pd.read_csv('/data/data_transposed.csv', index_col=0)

print(df_data.index)

centroid_manual = df_data.loc[['D1', 'D10']].values  
kmeans = KMeans(n_clusters=2, init=centroid_manual, n_init=1, random_state=42)
labels = kmeans.fit_predict(df_data)

df_data['cluster'] = labels
df_data.to_csv('/data/hasil_clustering.csv')
print(df_data[['cluster']])