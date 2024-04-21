from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html

from src import static_dir
from src.pages.generator import router as generator_router
from src.pages.materials import router as materials_router
from src.pages.work import router as work_router

app = FastAPI()

app.mount('/static', StaticFiles(directory=static_dir), name='static')

app.include_router(work_router, prefix='/api/work')
app.include_router(materials_router, prefix='/api/materials')
app.include_router(generator_router, prefix='/api/generator')


@app.get('/')
async def redirect_fastapi():
    return RedirectResponse(url='/work/first', status_code=302)


paths = ['/', '/work', '/api']
for path in paths:
    app.get(path)(redirect_fastapi)


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
