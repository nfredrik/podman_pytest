import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Exempel på error-loggar
error_logs = [
    "hejhopp",
    "ok det hjalper"
    "DatabaseError: Connection lost to MySQL server.",
    "ValueError: Cannot convert string to float.",
    "TypeError: Expected int but got str.",
    "APIError: Failed to retrieve response from endpoint.",
    "ConnectionError: Timeout occurred while fetching data.",
    "IndexError: List index out of range.",
    "KeyError: Missing required field in JSON.",
    "TypeError: Unsupported operand types for +: 'str' and 'int'."
]

# Vektorisera texten
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(error_logs).toarray()

# Klustring med K-Means
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(X)

# Reducera dimensioner med PCA för visualisering
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Skapa en DataFrame med klusterinformation
df = pd.DataFrame({"Error_Log": error_logs, "Cluster": labels})

# Visa vilka fel som tillhör vilka kluster
print(df.sort_values("Cluster"))

# Visualisering av kluster
plt.figure(figsize=(10, 5))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="viridis", edgecolors="k")
for i, txt in enumerate(error_logs):
    plt.annotate(txt[:15], (X_pca[i, 0], X_pca[i, 1]), fontsize=8)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Error Categorization with PCA")
plt.show()
