from fastapi import FastAPI
import media, location, interactionLog, auth, user
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(media.router)
app.include_router(location.router)
app.include_router(interactionLog.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)