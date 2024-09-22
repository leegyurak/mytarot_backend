import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import tarot
from containers import Container


app: FastAPI = FastAPI()
app.include_router(tarot)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.container = Container()

@app.get('/')
async def healthcheck():
    return {'ping': 'pong'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
