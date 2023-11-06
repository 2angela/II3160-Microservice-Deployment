from fastapi import FastAPI
from media import app as media
from location import app as location
from interactionLog import app as interactionLog
import uvicorn

app = FastAPI()

app.mount("/media", media)
app.mount("/location", location)
app.mount("/interactionLog", interactionLog)

if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=8000)