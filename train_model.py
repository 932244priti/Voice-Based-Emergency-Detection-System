import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------------
# 1. Load Dataset
# -----------------------------------

data = pd.read_csv("emergency_voice_dataset.csv")

print("\nDataset Loaded Successfully!")
print("Total Records:", len(data))

print("\nClass Distribution:")
print(data["label"].value_counts())


# -----------------------------------
# 2. Prepare Data
# -----------------------------------

X = data["text"]
y = data["label"]


# -----------------------------------
# 3. Split Dataset
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 4. TF-IDF
# -----------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    max_features=3000
)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)


# -----------------------------------
# 5. Train Logistic Regression
# -----------------------------------

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(
    X_train_vectorized,
    y_train
)


# -----------------------------------
# 6. Test Model
# -----------------------------------

predictions = model.predict(X_test_vectorized)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n===================================")
print("MODEL TRAINING COMPLETED")
print("===================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# -----------------------------------
# 7. Save Model
# -----------------------------------

with open(
    "emergency_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


with open(
    "vectorizer.pkl",
    "wb"
) as file:

    pickle.dump(
        vectorizer,
        file
    )


print("\n===================================")
print("FILES SAVED SUCCESSFULLY")
print("===================================")

print("✅ emergency_model.pkl")
print("✅ vectorizer.pkl")


# -----------------------------------
# 8. Test Real Examples
# -----------------------------------

test_sentences = [

    "Help me with my homework",

    "Help me carry this bag",

    "I think someone is watching me",

    "I feel uncomfortable here",

    "Help me someone is following me",

    "I am being attacked please help"

]

test_vectors = vectorizer.transform(
    test_sentences
)

test_predictions = model.predict(
    test_vectors
)

test_probabilities = model.predict_proba(
    test_vectors
)


print("\n===================================")
print("CONTEXT TEST")
print("===================================")

for sentence, prediction, probability in zip(
    test_sentences,
    test_predictions,
    test_probabilities
):

    confidence = max(probability) * 100

    print("\nSentence:", sentence)
    print("Prediction:", prediction.upper())
    print(
        "Confidence:",
        round(confidence, 2),
        "%"
    )