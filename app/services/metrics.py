import pandas as pd
from typing import Dict, Any



def safe_float(value):
    """
    Converts NaN or infinite values to None for JSON safety.
    """
    if pd.isna(value):
        return None
    return round(float(value), 2)

def calculate_metrics(df:pd.dataframe)  -> Dict[str, Any]:
    
    metrics = {
        "dataset" : {},
        "columns" : {}
    }

    metrics["dataset"] = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "missing_cells": int(df.isna().sum().sum())
    } 
    
    for column in df.columns:
        col_data = df[column]
        col_metrics = {}

        # Empty cells

        col_metrics["missing_count"] = int(col_data.isna().sum())
        col_metrics["missing_percentage"] = round(
            (col_metrics["missing_count"]/len(df))*100, 2
        )

        # Detect column type

        if pd.api.types.is_numeric_dtype(col_data):
            col_metrics["min"] = safe_float(col_data.min())
            col_metrics["max"] = safe_float(col_data.max())
            col_metrics["mean"] = safe_float(col_data.mean())
            col_metrics["median"] = safe_float(col_data.median())
            col_metrics["std"] = safe_float(col_data.std())

        elif pd.api.types.is_datetime64_any_dtype(col_data):
            col_metrics["type"] = "datetime"
            col_metrics["min_date"] = str(col_data.min())
            col_metrics["max_date"] = str(col_data.max())
            col_metrics["range_days"] = (col_data.max() - col_data.min()).days

        else:
            col_metrics["type"] = "categorical"
            value_counts = col_data.value_counts(dropna=True)
            col_metrics["unique_values"] = int(col_data.nunique())
            col_metrics["top_values"] = value_counts.head(5).to_dict()

        
        metrics["columns"][column] = col_metrics
    
    return metrics
    

    