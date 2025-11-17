
import os
import time
import uuid
import jwt

import uvicorn
from fastapi import FastAPI, Form, UploadFile, File, Request, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jwt import ExpiredSignatureError, InvalidTokenError

from models.models import movietop, User
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

templates=Jinja2Templates(directory="./templates")





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

@app.get('/form', response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/confirm')
async def create_film(name:str = Form(...), director:str = Form(...), price:int = Form(...), check:bool=Form(None)):
    if check is None:
        check_val=False
    else:
        check_val=True
    return {"name": name, "director":director, "price":price, "Russian":check_val}

@app.get('/fileupload', response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("file_input.html", {"request": request})


@app.post("/files/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join("images", file.filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return HTMLResponse(content=f"""
    <html>
        <body>
            <img src="/app/images/{file.filename}" alt="{file.filename}">
        </body>
    </html>
    """)


#Задание В

USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]

active_tokens={}
usernames={}

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def is_token_valid(token: str):
    if token in active_tokens:
        token_time=active_tokens[token]
        if time.time()-token_time<120:
            return True
    return False

@app.get('/login', response_class=HTMLResponse)
async def login_form():
    return """
    <form action="/login" method="post">
        <input type="text" id="name" name="name" required>
        <input type="password" id="password" name="password" required>

        <button type="submit">Войти</button>
    </form>"""

@app.post('/login')
async def login(name: str=Form(), password:str=Form()):
    user=get_user_from_db(name)
    if user and user.password==password:
        session_token=str(uuid.uuid4())
        active_tokens[session_token]=time.time()

        usernames[session_token]=name

        response=RedirectResponse(url='/user', status_code=303)
        response.set_cookie(httponly=True, secure=True, key='session_token', value=session_token)
        return response

@app.get('/user')
async def user_profile(session_token: str=Cookie(None)):
    if not session_token or not is_token_valid(session_token):
        return {"message": "Unauthorized"}
    active_tokens[session_token]=time.time()
    return {"username": usernames[session_token],
            "time": time.strftime("%y-%m-%d %H:%M:%S", time.localtime(active_tokens[session_token])),
            "films": {1: film1,
             2: film2,
             3: film3,
             4: film4,
             5: film5,
             6: film6,
             7: film7,
             8: film8,
             9: film9,
             10: film10,
             }
    }


#Задание Г

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="loginJWT")

SECRET_KEY='mysecretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 2

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + 60*ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    print('get user')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

@app.post('/loginJWT')
async def login(user_in: User):
    for user in USER_DATA:
        if user.username== user_in.username and user.password == user_in.password:
            token = create_jwt_token({"sub": user_in.username})
            print({"access_token": token, "token_type": "bearer"})
            return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}

@app.post('/add_film')
async def add_film(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    # Если пользователь не найден, возвращаем ошибку
    return {"error": "User not found"}
















if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8165)