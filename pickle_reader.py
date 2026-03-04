import pandas as pd

df = pd.read_pickle("Dataset/breathing_dataset.pkl")

print(len(df.airflow[1]))