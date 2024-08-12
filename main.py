from fastapi import FastAPI
from api.routes import devices, attributes, values


app = FastAPI()

app.include_router(devices.router)
app.include_router(attributes.router)
app.include_router(values.router)

@app.get("/")
async def index():
    return {"message": "API LCD Devices"}