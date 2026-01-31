from fastapi import FastAPI, UploadFile, File
import pandas as pd

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
    df = pd.read_csv(file.file)

    validation = validate_dataframe(df)
    if not validation["is_valid"]:
        return {"validation" : validation}

    metrics = calculate_metrics(df)
    # summary = generate_summary(metrics) //openAi

    summary = generate_ai_summary(metrics) // OllamaClient


    return {
        "validation" : validation,
        "metrics" : metrics,
        "ai_summary" : summary
    }

