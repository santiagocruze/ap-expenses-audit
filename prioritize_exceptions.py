import pandas as pd

exc = pd.read_csv("exceptions.csv")

# rank: High first, then Medium, then Low
risk_rank = {"High": 0, "Medium": 1, "Low": 2}
exc["risk_rank"] = exc["risk_level"].map(risk_rank).fillna(9)

cols = ["test_id","rule_name","risk_level","reason","txn_datetime","card_id","merchant","category","amount"]

exc = exc.sort_values(["risk_rank","test_id","txn_datetime"])
exc = exc[cols]

exc.head(50).to_csv("top_50_exceptions.csv", index=False)