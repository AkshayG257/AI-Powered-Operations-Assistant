def calculate_metrics(df):
    return {
        "total_requests" : int(df["requests"].sum()),
        "total_cost" : float(df["cost"].sum()),
        "average_cost_per_request" : round(
            df["requests"].sum() / df["cost"].sum(), 2
        )

    }