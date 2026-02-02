import pandas as pd
from typing import Dict


def validate_dataframe(df: pd.dataFrame) -> Dict:


    if df is None:
        return { 
            "is_valid" : False,
            "error" : "No data found"
        }

    if df.empty:
        return { 
            "is_valid" : False,
            "error" : "Uploaded file is empty"
        }

    # at least one column
    if df.shape[1] == 0 :
        return { 
            "is_valid" : False,
            "error" : "No columns found in file"
        }
    
    info = {
        "rows" : int(df.shape[0]),
        "columns" : int(df.shape[1]),
        "column_names" : list(df.columns)
    }

    return {
        "is_valid" : True,
        "info" : info
    }
    # 02022026 
    # required_columns = ["date","department","requests","cost"]
    # for col in required_columns:
    #     if col not in df.columns:
    #         errors.append("Missing column:{col}")

    # if "request" in df.columns and (df["requests"] < 0).any():
    #     errors.append("Request contains negative values")

    # if "cost" in df.columns and (df["cost"] < 0).any():
    #     errors.append("Costs contain negative values")

    # return {
    #     "is_valid" : len(errors) == 0,
    #     "errors" : errors
    # }        