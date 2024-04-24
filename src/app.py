import typing as _t

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

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


def prebuilt_html_patched(
    *,
    title: str = '',
    api_root_url: _t.Union[str, None] = None,
    api_path_mode: _t.Union[_t.Literal['append', 'query'], None] = None,
    api_path_strip: _t.Union[str, None] = None,
) -> str:
    """
    Returns a simple HTML page which includes the FastUI react frontend, loaded from https://www.jsdelivr.com/.

    Arguments:
        title: page title
        api_root_url: the root URL of the API backend, which will be used to get data, default is '/api'.
        api_path_mode: whether to append the page path to the root API request URL, or use it as a query parameter,
            default is 'append'.
        api_path_strip: string to remove from the start of the page path before making the API request.

    Returns:
        HTML string which can be returned by an endpoint to serve the FastUI frontend.
    """
    meta_extra = []
    if api_root_url is not None:
        meta_extra.append(f'<meta name="fastui:APIRootUrl" content="{api_root_url}" />')
    if api_path_mode is not None:
        meta_extra.append(
            f'<meta name="fastui:APIPathMode" content="{api_path_mode}" />'
        )
    if api_path_strip is not None:
        meta_extra.append(
            f'<meta name="fastui:APIPathStrip" content="{api_path_strip}" />'
        )
    meta_extra_str = '\n    '.join(meta_extra)
    # language=HTML
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <script type="module" crossorigin src="http://127.0.0.1:8000/get-js-file"></script>
    <link rel="stylesheet" crossorigin href="http://127.0.0.1:8000/get-css-file">
    {meta_extra_str}
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""


@app.get('/get-js-file')
async def get_js_file():
    # Указываем путь к файлу относительно корня проекта
    file_path = f'{static_dir}/index.js'
    return FileResponse(
        path=file_path, media_type='application/javascript', filename='index.js'
    )


@app.get('/get-css-file')
async def get_css_file():
    # Указываем путь к файлу относительно корня проекта
    file_path = f'{static_dir}/index.css'
    return FileResponse(path=file_path, media_type='text/css', filename='style.css')


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html_patched(title='FastUI Demo'))
