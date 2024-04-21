import webbrowser

import uvicorn

from src.app import app

try:
    uvicorn.run(app)
finally:
    webbrowser.open('http://127.0.0.1:8000/materials/materials')
