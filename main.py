from fastapi import FastAPI
import media, location, interactionLog, OAuth
import uvicorn

app = FastAPI()

app.include_router(OAuth.router)
app.include_router(media.router)
app.include_router(location.router)
app.include_router(interactionLog.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)