from fastapi import FastAPI
from .api import api

app = FastAPI(
    title='API-сервис',
    description='Выгрузка информации для сайта ric018.ru',
    version='1.0.0',    
)

app.include_router(api.router)


@app.get("/", description='')
async def root():
    return {"message": "Hello API Buffer Applications!"}

