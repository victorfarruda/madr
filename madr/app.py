from fastapi import FastAPI

from madr.routers import books

app = FastAPI()

app.include_router(books.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
