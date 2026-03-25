import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

df = pd.read_pickle("Dataset/breathing_dataset.pkl")

X = []
y = []

scaler = StandardScaler()

for i in range(len(df)):
    
    window = df.iloc[i]["window"]   # your combined signal
    
    # flatten (important)
    window_flat = np.array(window).flatten()
    
    X.append(window_flat)
    y.append(df.iloc[i]["label"])

X = np.array(X)
y = np.array(y)

le = LabelEncoder()
y = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

lr = LogisticRegression(max_iter=2000, class_weight='balanced')
lr.fit(X_train, y_train)

y_pred= lr.predict(X_test)

print(classification_report(y_test, y_pred, target_names=le.classes_))