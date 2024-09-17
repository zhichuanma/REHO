import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

df = pd.read_csv('results_normalized.csv')

correlation_matrix = df.corr(method='pearson', numeric_only=True)

kmeans = KMeans(n_clusters=5, random_state=0)
clusters = kmeans.fit_predict(correlation_matrix)

pca = PCA(n_components=2)
pca_results = pca.fit_transform(correlation_matrix.values)  # Use .values to get NumPy array

df_pca = pd.DataFrame({
    'PCA1': pca_results[:, 0],
    'PCA2': pca_results[:, 1],
    'Indicator': correlation_matrix.columns,
    'Cluster': clusters
})

plt.figure(figsize=(10, 8))

sns.scatterplot(
    x='PCA1', y='PCA2',
    hue='Cluster',
    palette='Set2',
    data=df_pca,
    s=100,
    legend='full'
)


for i in range(df_pca.shape[0]):
    plt.text(df_pca['PCA1'][i], df_pca['PCA2'][i], df_pca['Indicator'][i], fontsize=10, ha='right')

plt.title('K-Means Clustering of Indicators (5 Clusters)')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.show()
