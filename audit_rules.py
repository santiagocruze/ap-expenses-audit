import pandas as pd

df = pd.read_csv("transactions_clean.csv")

# Types
df["txn_datetime"] = pd.to_datetime(df["txn_datetime"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Helper columns
df["txn_date"] = df["txn_datetime"].dt.date
df["hour"] = df["txn_datetime"].dt.hour
df["is_weekend"] = df["txn_datetime"].dt.weekday >= 5

exceptions = []

def add_rule(mask, test_id, rule_name, risk_level, reason):
    cols = ["txn_datetime", "txn_date", "card_id", "merchant", "category", "amount"]
    out = df.loc[mask, cols].copy()
    out["test_id"] = test_id
    out["rule_name"] = rule_name
    out["risk_level"] = risk_level
    out["reason"] = reason
    exceptions.append(out)

# Context rules (low/medium risk; noisy but useful)
add_rule(df["is_weekend"], "T00", "WEEKEND_TXN", "Low", "Transaction on Saturday/Sunday")
add_rule((df["hour"] < 6) | (df["hour"] >= 21), "T00", "AFTER_HOURS_TXN", "Low", "Outside 06:00–21:00")

# T01 Exact duplicates
dup_key = ["card_id", "merchant", "amount", "txn_date"]
add_rule(df.duplicated(subset=dup_key, keep=False),
         "T01", "DUPLICATE_TXN", "High",
         "Exact duplicate: same card+merchant+amount+date")

# T02 High amount outliers (top 1%)
p99 = df["amount"].quantile(0.99)
add_rule(df["amount"] >= p99,
         "T02", "HIGH_AMOUNT_P99", "High",
         f"Amount is in top 1% (>= {p99:.2f})")

# T03 Velocity: many txns per card per day
txns_per_card_day = df.groupby(["card_id", "txn_date"]).size().rename("txn_count").reset_index()
fast = txns_per_card_day[txns_per_card_day["txn_count"] > 10]
df = df.merge(fast, on=["card_id", "txn_date"], how="left")  # adds txn_count where applicable

add_rule(df["txn_count"].notna(),
         "T03", "VELOCITY_CARD_DAY", "High",
         "Card has > 10 transactions in the same day")

# T04 Split transactions: same card+merchant+day, many txns and high total
grp = df.groupby(["card_id", "merchant", "txn_date"])["amount"].agg(["count", "sum"]).reset_index()
split = grp[(grp["count"] >= 3) & (grp["sum"] >= 500)]
df = df.merge(split, on=["card_id", "merchant", "txn_date"], how="left", suffixes=("", "_split"))

add_rule(df["sum"].notna(),
         "T04", "SPLIT_TXN", "High",
         "Same card+merchant+day has >=3 txns and total >= 500 (possible split)")

# Save outputs 
exceptions_df = pd.concat(exceptions, ignore_index=True)

# Sort: high risk first
risk_order = {"High": 0, "Medium": 1, "Low": 2}
exceptions_df["risk_rank"] = exceptions_df["risk_level"].map(risk_order).fillna(9)
exceptions_df = exceptions_df.sort_values(["risk_rank", "test_id", "txn_datetime"]).drop(columns=["risk_rank"])

exceptions_df.to_csv("exceptions.csv", index=False)

summary = (exceptions_df
           .groupby(["test_id", "rule_name", "risk_level"])
           .size()
           .reset_index(name="count")
           .sort_values(["risk_level", "count"], ascending=[True, False]))

total = len(df)
summary["pct_of_all_txns"] = (summary["count"] / total * 100).round(2)

summary.to_csv("exceptions_summary.csv", index=False)

print("Saved exceptions.csv and exceptions_summary.csv")
print(summary.head(20))