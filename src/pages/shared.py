from __future__ import annotations as _annotations

import json
from typing import Literal

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent
from pydantic import TypeAdapter, create_model

from src import data_dir
from src.schemas import FirstElement


def base_page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    return [
        c.PageTitle(text='ЛР №3Э'),
        c.Navbar(
            title='ЛР №3Э',
            title_event=GoToEvent(url='/materials'),
            start_links=[
                c.Link(
                    components=[c.Text(text='Теоритические материалы')],
                    on_click=GoToEvent(url='/materials/materials'),
                    active='startswith:/materials',
                ),
                c.Link(
                    components=[c.Text(text='Эксперементальная часть')],
                    on_click=GoToEvent(url='/work/first'),
                    active='startswith:/work',
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='Безопасность жизнедеятельности',
            links=[
                c.Link(
                    components=[c.Text(text='МТУСИ')],
                    on_click=GoToEvent(url='https://mtuci.ru/'),
                ),
            ],
        ),
    ]


## ----------------first--------------------


## ----------------second--------------------
