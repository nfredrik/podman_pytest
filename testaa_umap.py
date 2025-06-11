import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import umap
from sklearn.cluster import KMeans

# Exempel på error-loggar
error_logs = [
    "DatabaseError: Connection lost to MySQL server.",
    "ValueError: Cannot convert string to float.",
    "TypeError: Expected int but got str.",
    "APIError: Failed to retrieve response from endpoint.",
    "ConnectionError: Timeout occurred while fetching data.",
    "IndexError: List index out of range.",
    "KeyError: Missing required field in JSON.",
    "TypeError: Unsupported operand types for +: 'str' and 'int'."
]

# Vektorisera texten med TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(error_logs).toarray()  # Gör om till NumPy-array

# **1. PCA för att reducera till 2D**
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# **2. UMAP för avancerad 2D-reduktion**
umap_reducer = umap.UMAP(n_components=2)
X_umap = umap_reducer.fit_transform(X)

# K-Means för klustring
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels_pca = kmeans.fit_predict(X_pca)
labels_umap = kmeans.fit_predict(X_umap)

# **Visualisering av PCA-kluster**
plt.figure(figsize=(10, 5))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels_pca, cmap="viridis", edgecolors="k")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Error Categorization with PCA")
plt.show()

# **Visualisering av UMAP-kluster**
plt.figure(figsize=(10, 5))
plt.scatter(X_umap[:, 0], X_umap[:, 1], c=labels_umap, cmap="coolwarm", edgecolors="k")
plt.xlabel("UMAP Component 1")
plt.ylabel("UMAP Component 2")
plt.title("Error Categorization with UMAP")
plt.show()
