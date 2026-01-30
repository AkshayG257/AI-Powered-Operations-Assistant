def validate_dataframe(df):
    errors = []

    required_columns = ["date","department","requests","cost"]
    for col in required_columns:
        if col not in df.columns:
            errors.append("Missing column:{col}")

    if "request" in df.columns and (df["requests"] < 0).any():
        errors.append("Request contains negative values")

    if "cost" in df.columns and (df["cost"] < 0).any():
        errors.append("Costs contain negative values")

    return {
        "is_valid" : len(errors) == 0,
        "errors" : errors
    }        