import pandas as pd

df = pd.read_csv("iemocap_session1.csv")
df2 = pd.read_csv("iemocap_session2.csv")
df3 = pd.read_csv("iemocap_session3.csv")
df4 = pd.read_csv("iemocap_session4.csv")
df5 = pd.read_csv("iemocap_session5.csv")

df_combined = pd.concat([df, df2, df3, df4, df5], ignore_index=True)

df_combined.to_csv("iemocap_combined.csv", index=False)