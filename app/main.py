# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models.models import movietop





app = FastAPI()

app.mount("/app/images", StaticFiles(directory="images"), name="images")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/study", response_class=HTMLResponse)
async def root():
    html_content = """
        <html>
            <head>
                <title></title>
            </head>
            <body>
                <h1>Брянский Государственный Инженерно-Технологический Университет</h1>
                <img src="/app/images/bgitu.jpg" alt="">
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)

film1 = movietop(name='1+1', id=1, cost=999, director='Оливье Накаш')
film2 = movietop(name='Интерстеллар', id=2, cost=999, director='Кристофер Нолан')
film3 = movietop(name='Побег из Шоушенка', id=3, cost=999, director='Фрэнк Дарабонт')
film4 = movietop(name='Джентельмены', id=4, cost=999, director='Гай Ричи')
film5 = movietop(name='Зеленая миля', id=5, cost=999, director='Фрэнк Дарабонт')
film6 = movietop(name='Остров проклятых', id=6, cost=999, director='Мартин Скорсезе')
film7 = movietop(name='Властелин колец', id=7, cost=999, director='Питер Джексон')
film8 = movietop(name='Форрест Гамп', id=8, cost=999, director='Роберт Земекис')
film9 = movietop(name='Терминатор 2', id=9, cost=999, director='Джеймс Кэмерон')
film10 = movietop(name='Зеленая книга', id=10, cost=999, director='Питер Фарелли')

@app.get('/movietop')
async def movies():
    return {1:film1,
            2:film2,
            3: film3,
            4: film4,
            5: film5,
            6: film6,
            7: film7,
            8: film8,
            9: film9,
            10: film10,
            }

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8165)