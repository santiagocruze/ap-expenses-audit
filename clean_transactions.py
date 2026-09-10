import pandas as pd
import numpy as np
import openpyxl as px

RAW_PATH = "credit_card_transactions.csv"

df = pd.read_csv(RAW_PATH)

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

print(df.columns.tolist())

df = df.rename(columns={
    "trans_date_trans_time": "txn_datetime",
    "cc_num": "card_id",
    "amt": "amount",
    "first": "first_name",
    "last": "last_name",
})

df.to_csv("transactions_clean.csv", index=False)