from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Exempeldata
transactions = ["ICA KVANTUM", "OKQ8", "Spotify", "Folksam", "Pizza Hut","HEMKOP"]
labels = ["Mat & Dagligvaror", "Transport", "Abonnemang", "Boende", "Restaurang",'Övrigt']

# Skapa en modell för textklassificering
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(transactions, labels)

# Klassificera ny transaktion
print(model.predict(["HEMKÖP SOLNA C"]))  # Försöker avgöra kategori
