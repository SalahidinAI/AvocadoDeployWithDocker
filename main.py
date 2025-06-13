from fastapi import FastAPI
import uvicorn
from mysite.api.endpoints import avocado

avocado_app = FastAPI(title='Avocado')
avocado_app.include_router(avocado.avocado_router)


if __name__ == '__main__':
    uvicorn.run(avocado_app, host='127.0.0.1', port=8000)