from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

df = None


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    global df
    df = pd.read_csv(file.file)
    return {"message": "CSV uploaded successfully"}


@app.get("/summary")
def summary():
    if df is None:
        return {}

    total = len(df)
    left = len(df[df["Attrition"] == "Yes"])

    return {
        "totalEmployees": total,
        "employeesLeft": left,
        "attritionRate": round((left / total) * 100, 2),
        "averageTenure": round(df["Tenure"].mean(), 2)
    }


@app.get("/attrition-trend")
def attrition_trend():
    if df is None:
        return []

    trend = (
        df.groupby("Year")["Attrition"]
        .apply(lambda x: (x == "Yes").sum())
        .reset_index()
        .rename(columns={"Attrition": "count"})
    )

    return trend.to_dict(orient="records")

@app.get("/division-attrition")
def division_attrition():
    if df is None:
        return []

    data = (
        df[df["Attrition"] == "Yes"]
        .groupby("Division")
        .size()
        .reset_index(name="count")
    )

    return data.to_dict(orient="records")













