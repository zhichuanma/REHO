import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('results_normalized.csv')

# Calculate the Pearson correlation matrix
correlation_matrix = df.corr(method='pearson')

correlation_matrix.to_csv('correlation_matrix.csv', index=False)
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Heatmap of Correlation Matrix")
plt.show()

# K means cluster

kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(correlation_matrix)

df_clusters = pd.DataFrame({
    'Index': range(1, len(clusters) + 1),
    'Indicator': correlation_matrix.columns,
    'Cluster': clusters
})

# Select one indicator from each cluster
representative_indicators = df_clusters.groupby('Cluster')['Indicator'].first()
print("Selected representative indicators from each cluster:")
print(representative_indicators)


