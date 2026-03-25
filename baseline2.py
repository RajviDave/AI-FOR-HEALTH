import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
import collections


from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier


# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_pickle("Dataset/breathing_dataset.pkl")
df = df[df["label"] != "Body event"]

ros = RandomOverSampler(random_state=42)
# -------------------------------
# Prepare features (X) and labels (y)
# -------------------------------
X = []
y = []

for i in range(len(df)):
    window = df.iloc[i]["window"]
    
    # flatten signal
    window_flat = np.array(window).flatten()
    
    X.append(window_flat)
    y.append(df.iloc[i]["label"])

X = np.array(X)
y = np.array(y)


# -------------------------------
# Encode labels
# -------------------------------
le = LabelEncoder()
y = le.fit_transform(y)


# -------------------------------
# Train-test split (IMPORTANT)
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train, y_train = ros.fit_resample(X_train, y_train)
# -------------------------------
# Random Forest model
# -------------------------------
rf = RandomForestClassifier(
    n_estimators=300,
    class_weight='balanced_subsample',
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1                # use all CPU cores
)


# -------------------------------
# Train
# -------------------------------
rf.fit(X_train, y_train)


# -------------------------------
# Predict
# -------------------------------
y_pred = rf.predict(X_test)


# -------------------------------
# Evaluate
# -------------------------------
print(classification_report(
    y_test,
    y_pred,
    labels=np.unique(y_test),
    target_names=le.inverse_transform(np.unique(y_test))
))

print(collections.Counter(y_train))