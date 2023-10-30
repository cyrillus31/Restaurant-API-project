from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from .database import engine, init_db
from .routers import dishes, getall, menus, submenus

app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)
app.include_router(getall.router)

start_page_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Cyrillus' Restaurnat API Project</title>
    </head>
    <body>
        <h2>Restaurant API Project</h2>
        <p1>The docs for this API can be found <a href="http://cyrillus-restaurant-api.fvds.ru/docs"><b>here</b></a>.</p1>
        <br><br>
        <p2>Visit <a href="https://github.com/cyrillus31/Restaurant-API-project"><b>github page</b></a> of this project to learn more.</p2>
    </body>
</html>
"""

@app.on_event('startup')
async def on_startup():
    await init_db(engine)

@app.get('/')
def redirect_to_root():
    return RedirectResponse(url="/api/v1/")

@app.get('/api/v1/')
def root():
    return HTMLResponse(content=start_page_html)
