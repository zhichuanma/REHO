import pandas as pd

df = pd.read_csv('results_normalized.csv')

# Calculate the Pearson correlation matrix
correlation_matrix = df.corr(method='pearson')

correlation_matrix.to_csv('correlation_matrix.csv', index=False)
print(correlation_matrix)

threshold = 0

negative_relationships = {}

# Iterate over each row of the correlation matrix using iterrows()
for indicator, row in correlation_matrix.iterrows():
    # Find all labels (column names) with a correlation below the threshold in the current row
    negatives = row[row < threshold].index.tolist()
    negative_relationships[indicator] = negatives

# Convert the dictionary to a DataFrame
negative_relationships_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in negative_relationships.items()]))

# Display the DataFrame
print(negative_relationships_df)

csv_file_path = 'negative_relationships_df.csv'
negative_relationships_df.to_csv(csv_file_path, index=False)

# Convert the dictionary to a DataFrame for better visualization
print(negative_relationships)


