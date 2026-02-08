import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# 1. Loading dataset
data = pd.read_csv("ML/training_data.csv")

# Features
X = data[["change_percent", "avg_sentiment"]]

# Labels
y = data["label"]

# 2. Encoding labels (BUY / HOLD / SELL -> numbers)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 3. Spliting into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 4. Training the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. Evaluating the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 6. Saving model and encoder
joblib.dump(model, "ML/trading_model.pkl")
joblib.dump(label_encoder, "ML/label_encoder.pkl")

print("Model training complete and saved.")
