from fastapi import FastAPI
import media, location, interactionLog, auth, user, menu_ingredients_composition, customization, order, deliverOrder
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(media.router)
app.include_router(location.router)
app.include_router(interactionLog.router)
app.include_router(user.router)
app.include_router(menu_ingredients_composition.router)
app.include_router(customization.router)
app.include_router(order.router)
app.include_router(deliverOrder.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)