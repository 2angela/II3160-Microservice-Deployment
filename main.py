from fastapi import FastAPI
from media import app as media
from location import app as location
from interactionLog import app as interactionLog
# from OAuthApp import app as OAuthApp
# import media, location, interactionLog, OAuth
import uvicorn

app = FastAPI(debug=True)

# app.mount("/OAuth", OAuthApp)
app.mount("/media", media)
app.mount("/location", location)
app.mount("/interactionLog", interactionLog)
# app.include_router(OAuth.router)
# app.include_router(interactionLog.router)
# app.include_router(media.router)
# app.include_router(location.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)