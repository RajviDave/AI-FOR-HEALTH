import pandas as pd

#dataset reader
df = pd.read_pickle("Dataset/breathing_dataset.pkl")
print(len(df.window[1]))

#startind from scratch
#next step is hosting
#will start from tommorow