import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Exempeldata: Vanliga frågor och svar
train_texts = [
    "hello", "hi", "greetings",
    "what's the weather?", "how is the weather?",
    "goodbye", "bye", "see you"
]
train_labels = ["greeting", "greeting", "greeting", "weather", "weather", "farewell", "farewell", "farewell"]



# NLP-modell
nlp = spacy.load("en_core_web_sm")

# Konvertera text till numeriska vektorer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# Träna ML-modellen
model = MultinomialNB()
model.fit(X_train, train_labels)

def classify_message(message):
    X_test = vectorizer.transform([message])
    return model.predict(X_test)[0]

# Testa modellen
print(classify_message("hello"))  # Förväntat: greeting
print(classify_message("how's the weather?"))  # Förväntat: weather


print(classify_message("trombone"))  # Förväntat: greeting

print(classify_message("fredde"))  # Förväntat: greeting
