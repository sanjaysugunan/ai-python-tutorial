from fastapi import FastAPI, types
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/margin")
def margin(revenue: float, expenses: float):
    profit = revenue - expenses
    margin_percentage = (profit / revenue) * 100
    return {"profit": profit, "margin_percentage": margin_percentage}

# What the user must send us (the request body)
class Review(BaseModel):
    text: str

# What Gemini must give back
class Sentiment(BaseModel):
    label: str   # "positive", "negative", or "neutral"
    score: int    # 1(very bad) to 5(very good)

@app.post("/sentiment")
def analyze_sentiment(review: Review):
    response =  client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = ("Find the sentiment of this customer review."
                    "label must be 'positive', 'negative', or ''neutral."
                    "score must be a number from 1(very bad) to 5 (very good)."
                    f"Review: {review.text}"),
        config = types.GenerateContentConfig(
            response_mime_type = "application/json",  # reply in JSON
            response_schema =  Sentiment,
        ),
    )
    return response.parsed

