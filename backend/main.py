from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io
import matplotlib.pyplot as plt
from datetime import datetime

app = FastAPI()

@app.post("/upload")
async def upload_blood_test(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        return {"message": "File uploaded successfully", "columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/chart/{test_name}")
async def get_chart(test_name: str):
    # Dummy data
    dates = [datetime(2024, 1, i+1) for i in range(10)]
    levels = [50 + i * 5 for i in range(10)]
    
    plt.figure(figsize=(8, 4))
    plt.plot(dates, levels, marker="o", linestyle="-", color="b")
    plt.xlabel("Date")
    plt.ylabel(f"{test_name} Levels")
    plt.title(f"Trend for {test_name}")
    
    plt.savefig("chart.png")
    return {"message": "Chart generated"}
