from fastapi import FastAPI
from pydantic import BaseModel
from app.services.sales_service import process_lead

app = FastAPI(title="AI Sales Intelligence System")


class LeadRequest(BaseModel):
    company: str
    industry: str
    employees: int


@app.get("/")
def home():
    return {"message": "AI Sales Intelligence API running"}


@app.post("/analyze")
def analyze(data: LeadRequest):

    return process_lead(
        company=data.company,
        industry=data.industry,
        employees=data.employees
    )