from fastapi import FastAPI
import backend.buffer.api as api

app = FastAPI(
    title='API-сервис',
    description='Выгрузка информации для сайта ric018.ru',
    version='1.0.0',
)

app.include_router(api.router)


@app.get("/", description='Приветствие сервиса', tags=["Главный"], summary='Приветствие сервиса')
async def root() -> dict:
    return {"message": "Welcome to the API service"}
