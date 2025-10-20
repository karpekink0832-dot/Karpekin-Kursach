# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

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
                <h1>Hello from FastAPI!</h1>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8165)