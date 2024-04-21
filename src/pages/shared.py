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

UserListAdapter = TypeAdapter(dict[str, FirstElement])
with open(f'{data_dir}/data_1.json', encoding='UTF-8') as f:
    first_elemets = json.load(f)
    first_data = UserListAdapter.validate_python(first_elemets['data'])
    # print(first_data)

keys = list(first_data.keys())

variations = []
for material, info in first_data.items():
    v = [f'{material} [{tol.name}]' for tol in info.tol]
    variations.extend(v)

materials = Literal[*keys]

ChooseMaterialModel = create_model(
    'ChooseMaterialModel',
    material=(Literal[*variations], ...),
)

tols = {}
for key in keys:
    tols_names = [t.name for t in first_data[key].tol]
    ChooseTolModel = create_model('ChooseTolModel', tol=(Literal[*tols_names], ...))
    model = create_model('ChooseTolModel', tol=(Literal[*tols_names], ...))
    tols[key] = model


tols_dict = {}
for material, info in first_data.items():
    v = {tol.name: tol for tol in info.tol}
    tols_dict.update({material: v})


## ----------------second--------------------
