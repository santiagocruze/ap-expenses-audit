# AP/Expenses Audit — Duplicate + Fraud-Risk Testing Pack (Python)

## Overview
This project simulates a junior auditor / finance analyst workflow: take raw credit card/expense-style transactions, clean and standardize the data, run common fraud-risk/anomaly tests, and produce an **exceptions register** plus a **prioritized review list**.

The goal is not to “prove fraud,” but to **identify transactions that warrant follow-up**.

---

## Files in this Project

### Input
- `credit_card_transactions.csv`  
  Raw transaction dataset.

### Scripts
- `clean_transactions.py`  
  Cleans the raw dataset and outputs `transactions_clean.csv`.

- `audit_rules.py`  
  Runs audit tests on `transactions_clean.csv` and outputs:
  - `exceptions.csv`
  - `exceptions_summary.csv`

- `prioritize_exceptions.py`  
  Sorts exceptions by risk and outputs:
  - `top_50_exceptions.csv`

### Outputs (Deliverables)
- `transactions_clean.csv`  
  Cleaned dataset with standardized column names (e.g., `txn_datetime`, `card_id`, `amount`) and consistent types.

- `exceptions.csv`  
  **Exceptions register**: transactions flagged by at least one test, including:
  - `test_id` (workpaper-style test identifier)
  - `rule_name`
  - `risk_level` (High/Medium/Low)
  - `reason` (plain-English explanation)

- `exceptions_summary.csv`  
  Summary of exceptions by test/rule, including:
  - count of flagged transactions
  - `% of all transactions` (helps assess how noisy a test is)

- `top_50_exceptions.csv`  
  A prioritized shortlist for review (highest-risk first). This is the file a reviewer would open first.
  
- `audit_testing_pack.xlsx`  
  Single Excel deliverable with Summary, Top_50, Rules, and a sample of exceptions.


---


## How to Run
### Prerequisites
- Python 3 installed
- Install required packages:

```bash
pip install pandas numpy openpyxl
```

### Run the Pipeline (from the project folder)
1) **Clean + standardize columns** (creates `transactions_clean.csv`)
```bash
python clean_transactions.py
```

2) **Run audit tests** (creates `exceptions.csv` and `exceptions_summary.csv`)
```bash
python audit_rules.py
```

3) **Prioritize exceptions for review** (creates `top_50_exceptions.csv`)
```bash
python prioritize_exceptions.py
```

### Expected Output Files
After running the steps above, you should have:
- `transactions_clean.csv`
- `exceptions.csv`
- `exceptions_summary.csv`
- `top_50_exceptions.csv`
```