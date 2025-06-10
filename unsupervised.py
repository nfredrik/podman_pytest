import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Sample error logs
error_logs = [
    "DatabaseError: Connection lost to MySQL server.",
    "ValueError: Cannot convert string to float.",
    "TypeError: Expected int but got str.",
    "APIError: Failed to retrieve response from endpoint.",
    "ConnectionError: Timeout occurred while fetching data.",
    "IndexError: List index out of range.",
    "Olle i blabarskogen: List index out of range.",
    "Nisse i blabarskogen: List index out of range.",
    "KeyError: Missing required field in JSON.",
    "TypeError: Unsupported operand types for +: 'str' and 'int'."
]

# Convert errors into TF-IDF vectorized format
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(error_logs)

# Apply K-Means clustering (choose optimal number of clusters)
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Assign clusters to error messages
clusters = kmeans.labels_
df = pd.DataFrame({"Error_Log": error_logs, "Cluster": clusters})

# Print categorized errors
print(df.sort_values("Cluster"))

# Visualize clusters
plt.hist(clusters, bins=num_clusters, color="skyblue", edgecolor="black")
plt.xlabel("Error Categories")
plt.ylabel("Count")
plt.title("Categorization of Software Errors")
plt.show()
