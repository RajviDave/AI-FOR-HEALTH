import pandas as pd

df = pd.read_pickle("Dataset/breathing_dataset.pkl")

print(df.airflow[1])