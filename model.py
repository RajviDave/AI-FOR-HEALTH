import pandas as pd
import numpy as np
import torch
import torch.nn as nn

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

from torch.utils.data import TensorDataset, DataLoader, WeightedRandomSampler


# ----------------------------
# Load dataset
# ----------------------------

df = pd.read_pickle("Dataset/breathing_dataset.pkl")

# Merge rare classes
df.loc[df["label"] == "Body event", "label"] = "Normal"
df.loc[df["label"] == "Mixed Apnea", "label"] = "Normal"


# ----------------------------
# Prepare data
# ----------------------------

X = np.stack(df["window"].values)
y = df["label"].values
participants = df["participant"].values

# 🔥 Normalize each window (IMPORTANT)
X = (X - X.mean(axis=1, keepdims=True)) / (X.std(axis=1, keepdims=True) + 1e-6)

# Encode labels
le = LabelEncoder()
y = le.fit_transform(y)

print("Classes:", le.classes_)

# Convert to tensors
X = torch.tensor(X, dtype=torch.float32)
X = X.permute(0, 2, 1)   # (samples, channels, time)

y = torch.tensor(y, dtype=torch.long)


# ----------------------------
# Improved CNN Model
# ----------------------------

class CNN1D(nn.Module):

    def __init__(self, num_classes):
        super().__init__()

        self.conv_block = nn.Sequential(
            nn.Conv1d(2, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(32, 64, kernel_size=7, padding=3),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, kernel_size=5, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(2)
        )

        self.global_pool = nn.AdaptiveAvgPool1d(1)

        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.global_pool(x)
        x = x.squeeze(-1)
        x = self.fc(x)
        return x


# ----------------------------
# Leave-One-Participant-Out
# ----------------------------

unique_participants = np.unique(participants)

acc_list = []
prec_list = []
rec_list = []

for test_p in unique_participants:

    print("\nTesting on:", test_p)

    train_idx = participants != test_p
    test_idx = participants == test_p

    X_train = X[train_idx]
    X_test = X[test_idx]

    y_train = y[train_idx]
    y_test = y[test_idx]

    # 🔥 Weighted Sampling (IMPORTANT)
    class_counts = np.bincount(y_train.numpy())
    weights = 1. / class_counts
    sample_weights = weights[y_train.numpy()]

    sampler = WeightedRandomSampler(sample_weights, len(sample_weights))

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=32,
        sampler=sampler
    )

    test_loader = DataLoader(
        TensorDataset(X_test, y_test),
        batch_size=32
    )

    model = CNN1D(len(np.unique(y)))

    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
    criterion = nn.CrossEntropyLoss()

    # ----------------------------
    # Training
    # ----------------------------

    for epoch in range(40):

        model.train()
        total_loss = 0

        for xb, yb in train_loader:

            optimizer.zero_grad()

            preds = model(xb)

            loss = criterion(preds, yb)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    # ----------------------------
    # Testing
    # ----------------------------

    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():

        for xb, yb in test_loader:

            outputs = model(xb)

            preds = torch.argmax(outputs, dim=1)

            y_true.extend(yb.numpy())
            y_pred.extend(preds.numpy())

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)

    cm = confusion_matrix(y_true, y_pred)

    acc_list.append(acc)
    prec_list.append(prec)
    rec_list.append(rec)

    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("Confusion Matrix:\n", cm)


# ----------------------------
# Final Results
# ----------------------------

print("\nFinal Cross-Validation Results")

print("Average Accuracy:", np.mean(acc_list))
print("Average Precision:", np.mean(prec_list))
print("Average Recall:", np.mean(rec_list))