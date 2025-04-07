import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sunlit_terraces.routes import sunlight, venues

# Load environment variables
load_dotenv()
GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

app = FastAPI()

app.include_router(venues.router, prefix="/venues", tags=["Venues"])
app.include_router(sunlight.router, prefix="/sunlight", tags=["Sunlight"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sunlit Terraces API"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust to your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
