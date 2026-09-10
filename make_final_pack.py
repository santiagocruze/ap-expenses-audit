import pandas as pd

def safe_read_csv(path):
    """Read CSV if it exists; return None if not found."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return None

def main():
    summary = safe_read_csv("exceptions_summary.csv")
    top50 = safe_read_csv("top_50_exceptions.csv")
    exc = safe_read_csv("exceptions.csv")

    if summary is None or top50 is None:
        raise FileNotFoundError(
            "Missing required files. Run the pipeline first:\n"
            "  python clean_transactions.py\n"
            "  python audit_rules.py\n"
            "  python prioritize_exceptions.py"
        )
    
    exc_sample = None
    if exc is not None:
        exc_sample = exc.head(5000)

    rules = pd.DataFrame([
        {"test_id": "T01", "rule_name": "Exact duplicates", "risk_level": "High"},
        {"test_id": "T02", "rule_name": "High amount outliers", "risk_level": "High/Medium"},
        {"test_id": "T03", "rule_name": "Velocity (many txns/day)", "risk_level": "High"},
        {"test_id": "T04", "rule_name": "Split transactions", "risk_level": "High"},
        {"test_id": "T00", "rule_name": "Context (weekend/after-hours)", "risk_level": "Low"},
    ])

    out_path = "audit_testing_pack.xlsx"

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        top50.to_excel(writer, sheet_name="Top_50", index=False)
        rules.to_excel(writer, sheet_name="Rules", index=False)

        if exc_sample is not None:
            exc_sample.to_excel(writer, sheet_name="Exceptions_sample", index=False)

    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()