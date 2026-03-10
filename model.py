import pandas as pd
import numpy as np
import torch
import torch.nn as nn

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

from torch.utils.data import TensorDataset, DataLoader


# ----------------------------
# Load dataset
# ----------------------------

df = pd.read_pickle("Dataset/breathing_dataset.pkl")

# Merge extremely rare classes
df.loc[df["label"] == "Body event", "label"] = "Normal"
df.loc[df["label"] == "Mixed Apnea", "label"] = "Normal"


# ----------------------------
# Prepare data
# ----------------------------

X = np.stack(df["window"].values)
y = df["label"].values
participants = df["participant"].values

# Encode labels
le = LabelEncoder()
y = le.fit_transform(y)

print("Classes:", le.classes_)

# Convert to PyTorch tensors
X = torch.tensor(X, dtype=torch.float32)
X = X.permute(0, 2, 1)   # (samples, channels, time)

y = torch.tensor(y, dtype=torch.long)

# ----------------------------
# CNN Model
# ----------------------------

class CNN1D(nn.Module):

    def __init__(self, num_classes):

        super().__init__()

        self.conv1 = nn.Conv1d(2, 32, kernel_size=5)
        self.pool = nn.MaxPool1d(2)

        self.conv2 = nn.Conv1d(32, 64, kernel_size=5)

        self.fc1 = nn.Linear(64 * 237, 64)
        self.fc2 = nn.Linear(64, num_classes)

        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):

        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))

        x = x.view(x.size(0), -1)

        x = self.relu(self.fc1(x))
        x = self.dropout(x)

        x = self.fc2(x)

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

    # Compute class weights
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(y_train.numpy()),
        y=y_train.numpy()
    )

    weights = torch.tensor(class_weights, dtype=torch.float32)

    # Data loaders
    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=32,
        shuffle=True
    )

    test_loader = DataLoader(
        TensorDataset(X_test, y_test),
        batch_size=32
    )

    # Model
    model = CNN1D(len(np.unique(y)))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    criterion = nn.CrossEntropyLoss(weight=weights)

    # ----------------------------
    # Training
    # ----------------------------

    for epoch in range(10):

        model.train()

        for xb, yb in train_loader:

            optimizer.zero_grad()

            preds = model(xb)

            loss = criterion(preds, yb)

            loss.backward()

            optimizer.step()

    # ----------------------------
    # Test
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
# Average results
# ----------------------------

print("\nFinal Cross-Validation Results")

print("Average Accuracy:", np.mean(acc_list))
print("Average Precision:", np.mean(prec_list))
print("Average Recall:", np.mean(rec_list))