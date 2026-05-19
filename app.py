from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model import *
from datetime import datetime, date

# ================================================ Configurações iniciais de caminhos, objetos e FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="Static"), name="Static")
templates = Jinja2Templates(directory="Templates")

hospede = Hospede()


@app.get("/")
def root(request: Request):
    hospedes = hospede.listHospede()

    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request,
                                          "hospedes": hospedes
                                      }
                                      )