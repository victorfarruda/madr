from fastapi import FastAPI

from madr.routers import auth, books, novelists, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(novelists.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
