from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from typing import Dict

from app.utils.data_loader import load_csv
from app.services.metrics import calculate_metrics
from app.services.validator import validate_dataframe
from app.services.ai_summary import generate_summary,generate_ai_summary



app = FastAPI(title="AI ops assistant")

@app.get("/")
def health_check():
    return {"status":"running"}


@app.post("/analyze-file")
async def analyze_data(file: UploadFile = File(...)):
    # df = load_csv("data/sample_data.csv") // stattic test file

    filename = file.filename.lower()

    if not (filename.endswith(".csv") or filename.endswith(".xlsx") or filename.endswith(".xls")):
        raise HTTPException(
            status_code=400,
            detail = "Only csv or excel files are supported"
        )

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file.file, engine="openpyxl")
        elif filename.endswith(".xls"):
            df = pd.read_excel(file.file, engine="xlrd")

    except Exception as e:
        raise HTTPException(
            status_code = 400,
            detail = f"Failed to read file : {str(e)}"
        )


    validation = validate_dataframe(df)
    if not validation["is_valid"]:
        return {"validation" : validation}

    metrics = calculate_metrics(df)
    # summary = generate_summary(metrics) //openAi

    ai_summary = generate_ai_summary(metrics)


    return {
        "validation" : validation,
        "metrics" : metrics,
        "ai_summary" : ai_summary
    }

