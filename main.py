# FastAPI
from fastapi import FastAPI

# Custom
from models.users import User
from models.tweet import Tweet

app = FastAPI()


@app.get(
    path="/home"
)
def home():
    return {"Twitter API": "Working Fine"}
