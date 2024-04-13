import logging
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from pydantic import BaseModel
import numpy as np
import asyncio

from datetime import date
import enum
import sys
from typing import Annotated
import webbrowser
from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import SelectOption, fastui_form

from fastapi import FastAPI
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field
import uvicorn
from fastapi.staticfiles import StaticFiles

from .shared import base_page

app = FastAPI()
app.mount("/work/static", StaticFiles(directory="src/static"), name="static")


class ToolEnum(str, enum.Enum):
    hammer = "hammer"
    screwdriver = "screwdriver"
    saw = "saw"
    claw_hammer = "claw_hammer"


class SelectForm(BaseModel):
    select_single: ToolEnum = Field(title="Select Single")


class GraphData(BaseModel):
    text: str  # Текст для отображения на изображении
    # color: str  # Цвет фона или текста
    # font_size: int  # Размер шрифта текста


class Thing(BaseModel):
    lel: int
    kek: int


@app.post(
    "/api/generate-image", response_model=FastUI, response_model_exclude_none=True
)
async def generate_image(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    # async def generate_image(data):
    # Создаем график

    print(form)
    plt.figure()
    plt.plot([1, 2, 3], [1, 3, 3], label="Sample Data")
    plt.title("Sample Graph")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.legend()

    # Сохраняем график в файл
    if not os.path.exists("static"):
        os.makedirs("static")
    path = "src/static/generated_graph.png"
    plt.savefig(path)
    plt.close()

    return [
        c.Table(
            data=[Thing(kek=1, lel=1)],
            # data_model=Thing,
            columns=[
                DisplayLookup(
                    field="kek",
                    # on_click=GoToEvent(url="./{id}"),
                    # table_width_percent=33,
                ),
                DisplayLookup(field="lel", table_width_percent=33),
                # DisplayLookup(field="population", table_width_percent=33),
            ],
        ),
        c.Image(src="static/generated_graph.png"),
        c.Heading(text="Выберите следующий график", level=3),
        c.ModelForm(
            model=SelectForm,
            display_mode="default",
            submit_url="/api/generate-image",
            method="POST",
            submit_on_change=True,
            # submit_target="image_frame",
        ),
        # c.Button(
        #     text="Обратно к выбору",
        #     on_click=PageEvent(
        #         name="change-form",
        #         push_path="/work/first",
        #         context={"kind": "third"},
        #     ),
        # ),
    ]


@app.get(
    "/api/work/forms/{kind}", response_model=FastUI, response_model_exclude_none=True
)
def form_content(kind):
    return [
        c.Heading(text=f"Login Form{kind}", level=2),
        c.Paragraph(text="Simple login form with email and password."),
        c.Image(
            src="static/img.png",
            width="50%",
            class_name="d-flex justify-content-center",
        ),
        c.ModelForm(
            model=SelectForm,
            display_mode="default",
            submit_url="/api/generate-image",
            method="POST",
            submit_on_change=True,
            # submit_target="image_frame",
        ),
        # c.Form(
        #     form_fields=[
        #         c.FormFieldInput(name="text", title="Text", required=True),
        #         c.FormFieldInput(name="color", title="Color", required=True),
        #         c.FormFieldInput(
        #             name="font_size",
        #             title="Font Size",
        #             required=True,
        #             input_type="number",
        #         ),
        #     ],
        #     submit_url="/api/generate-image",  # URL для отправки данных формы
        #     # submit_method="post",  # Метод отправки данных
        #     footer=[
        #         c.Button(text="Submit", on_click=PageEvent(name="submit-form")),
        #     ],
        # ),
        # c.Button(text="Show Modal Form", on_click=PageEvent(name="modal-form")),
        # c.Modal(
        #     title="Modal Form",
        #     body=[
        #         c.Paragraph(text="Form inside a modal!"),
        #         c.Form(
        #             form_fields=[
        #                 c.FormFieldInput(name="foobar", title="Foobar", required=True),
        #             ],
        #             submit_url="/api/components/modal-form",
        #             footer=[],
        #             submit_trigger=PageEvent(name="modal-form-submit"),
        #         ),
        #     ],
        #     footer=[
        #         c.Button(
        #             text="Cancel",
        #             named_style="secondary",
        #             on_click=PageEvent(name="modal-form", clear=True),
        #         ),
        #         c.Button(text="Submit", on_click=PageEvent(name="modal-form-submit")),
        #     ],
        #     open_trigger=PageEvent(name="modal-form"),
        # ),
        # c.ModelForm(
        #     model=SelectForm,
        #     display_mode="default",
        #     submit_url="/api/vizualize/first",
        # ),
        # c.Modal(
        #     title="Static Modal",
        #     body=[
        #         c.Paragraph(
        #             text="This is some static content that was set when the modal was defined."
        #         ),
        #         c.ServerLoad(
        #             path="/vizualize/first",
        #             # load_trigger=PageEvent(name="change-form"),
        #             components=form_content(kind),
        #      return   ),
        #     ],
        #     footer=[
        #         c.Button(
        #             text="Close", on_click=PageEvent(name="static-modal", clear=True)
        #         ),
        #     ],
        #     open_trigger=PageEvent(name="static-modal"),
        # ),
    ]


@app.post(
    "/api/vizualize/first", response_model=FastUI, response_model_exclude_none=True
)
def vizualize_first(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    print(form)
    return [c.FireEvent(event=PageEvent(name="static-modal"))]
    # (
    #     c.Div(
    #         components=[
    #             c.Heading(text="Button and Modal", level=2),
    #             c.Paragraph(
    #                 text="The button below will open a modal with static content."
    #             ),
    #             c.Button(
    #                 text="Show Static Modal", on_click=PageEvent(name="static-modal")
    #             ),
    #             c.Button(
    #                 text="Secondary Button",
    #                 named_style="secondary",
    #                 class_name="+ ms-2",
    #             ),
    #             c.Button(
    #                 text="Warning Button", named_style="warning", class_name="+ ms-2"
    #             ),
    #         ],
    #         class_name="border-top mt-3 pt-1",
    #     ),
    # )


@app.get("/api/work/{kind}", response_model=FastUI, response_model_exclude_none=True)
def work(kind):
    return base_page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text="График 1")],
                    on_click=PageEvent(
                        name="change-form",
                        push_path="/work/first",
                        context={"kind": "first"},
                    ),
                    active="/first",
                ),
                c.Link(
                    components=[c.Text(text="График 2")],
                    on_click=PageEvent(
                        name="change-form",
                        push_path="/work/second",
                        context={"kind": "second"},
                    ),
                    active="/second",
                ),
                c.Link(
                    components=[c.Text(text="Задание 3")],
                    on_click=PageEvent(
                        name="change-form",
                        push_path="/work/third",
                        context={"kind": "third"},
                    ),
                    active="/third",
                ),
            ],
            mode="tabs",
            class_name="+ mb-4",
        ),
        c.ServerLoad(
            path="/work/forms/{kind}",
            load_trigger=PageEvent(name="change-form"),
            components=form_content(kind),
        ),
        title="Исследование звукоизоляции ограждающих конструкций",
    )
    # return base_page(
    #     c.Heading(text="Выберите номер графика", level=2),
    #     c.Div(
    #         components=[
    #             c.Paragraph(text="Тут будет крутое задание"),
    #             c.Button(text="Построить график"),
    #         ],
    #         class_name="border-top mt-3 pt-1",
    #     ),
    #     c.Div(
    #         components=[
    #             c.Paragraph(text="Тут будет крутое задание"),
    #             c.Button(text="Построить график"),
    #         ],
    #         class_name="border-top mt-3 pt-1",
    #     ),
    #     # title="Добро пожаловать!",
    # )


@app.get("/api/materials", response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(
        c.Heading(text="Теоритические материалы", level=2),
        c.Div(
            components=[
                c.Paragraph(text="Лабораторные работы на 2023-2024, яндекс диск:"),
                c.Link(
                    components=[c.Text(text="Ссылка на материалы к работе")],
                    on_click=GoToEvent(
                        url="https://disk.yandex.ru/d/DUkUCWzFp6rhjg", target="_blank"
                    ),
                ),
            ],
            class_name="border-top mt-3 pt-1",
        ),
        # title="Исследование звукоизоляции ограждающих конструкций",
    )


class_name = "mt-3 pl-3 pt-1"


# @app.get("/api/work", response_model=FastUI, response_model_exclude_none=True)
# def weloce_page() -> list[AnyComponent]:
#     return base_page(
#         c.Heading(text="Добро пожаловать!", level=2),
#         c.Image(src="/static/mtuci.jpg"),
#         c.Div(
#             components=[
#                 c.Button(text="Перейти к списку лабараторных работ"),
#             ],
#             class_name=class_name,
#         ),
#         c.Div(
#             components=[
#                 c.Button(text="Перейти к материалам"),
#             ],
#             class_name=class_name,
#         ),
#     )


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))


def main():
    # webbrowser.open("http://localhost:8000")
    uvicorn.run(app)
