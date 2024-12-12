"""Точка входа в приложение."""

# THIRDPARTY
from fastapi import FastAPI
import uvicorn

# FIRSTPARTY
from app.routers.territory import router

app = FastAPI(
    title='Тестовое задание для ДОМ.РФ',
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
