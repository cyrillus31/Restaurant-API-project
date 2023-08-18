from fastapi import FastAPI

from .database import engine, init_db
from .routers import dishes, getall, menus, submenus

app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)
app.include_router(getall.router)


@app.on_event('startup')
async def on_startup():
    await init_db(engine)


@app.get('/api/v1/')
def root():
    return {
        'message': 'Checkout the code at https://github.com/cyrillus31/YLab_Homework-1'
    }
