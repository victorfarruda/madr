from fastapi import FastAPI

from madr.routers import books, novelists

app = FastAPI()

app.include_router(books.router)
app.include_router(novelists.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
