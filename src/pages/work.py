import json
from typing import Annotated

from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup
from fastui.events import PageEvent
from fastui.forms import fastui_form
from matplotlib import pyplot as plt
from pydantic import TypeAdapter

from src import data_dir, static_dir
from src.pages.shared import base_page
from src.schemas import FirstElement, SelectForm

router = APIRouter()


@router.get('/forms/first', response_model=FastUI, response_model_exclude_none=True)
def first_form():
    return [
        c.Heading(text='Введите параметры', level=3, class_name='pb-3'),
        c.ModelForm(
            model=SelectForm,
            display_mode='default',
            submit_url='/api/work/generate_chart',
            method='POST',
            # submit_on_change=True,
        ),
    ]


UserListAdapter = TypeAdapter(dict[str, FirstElement])
with open(f'{data_dir}/first.json', encoding='UTF-8') as f:
    first_elemets = json.load(f)
    first_data = UserListAdapter.validate_python(first_elemets)
    print(first_data)


@router.post('/generate_chart', response_model=FastUI, response_model_exclude_none=True)
async def generate_image(form: Annotated[SelectForm, fastui_form(SelectForm)]):
    plt.figure()
    plt.plot([1, 2, 3], [1, 3, 3], label='Sample Data')
    plt.title('Sample Graph')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.legend()

    path = f'{static_dir}/generated_graph.png'
    plt.savefig(path)
    plt.close()
    element = first_data[form.material]

    # c.FireEvent(event=)

    return [
        c.Table(
            data=[element],
            columns=[
                DisplayLookup(field='Вес, кг'),
                DisplayLookup(field='63 Гц'),
                DisplayLookup(field='125 Гц'),
                DisplayLookup(field='250 Гц'),
                DisplayLookup(field='500 Гц'),
                DisplayLookup(field='1000 Гц'),
                DisplayLookup(field='2000 Гц'),
                DisplayLookup(field='4000 Гц'),
                DisplayLookup(field='8000 Гц'),
            ],
        ),
        c.Div(
            components=[
                c.Image(
                    src=f'/static/{element.img_name}',
                    width='50%',
                ),
                c.Image(src='/static/generated_graph.png', width='50%'),
            ],
        ),
        c.Div(
            components=[
                c.Button(
                    text='Обратно',
                    on_click=PageEvent(
                        name='change-form',
                        push_path='/work/first',
                        context={'kind': 'first'},
                    ),
                ),
            ],
            class_name='d-flex justify-content-center pt-3 ',
        ),
    ]


@router.get('/{kind}', response_model=FastUI, response_model_exclude_none=True)
def work(kind):
    return base_page(
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='График 1')],
                    on_click=PageEvent(
                        name='change-form',
                        push_path='/work/first',
                        context={'kind': 'first'},
                    ),
                    active='/first',
                ),
                c.Link(
                    components=[c.Text(text='График 2')],
                    on_click=PageEvent(
                        name='change-form',
                        push_path='/work/second',
                        context={'kind': 'second'},
                    ),
                    active='/second',
                ),
                c.Link(
                    components=[c.Text(text='Задание 3')],
                    on_click=PageEvent(
                        name='change-form',
                        push_path='/work/third',
                        context={'kind': 'third'},
                    ),
                    active='/third',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
        c.ServerLoad(
            path='/work/forms/{kind}',
            load_trigger=PageEvent(name='change-form'),
            components=form_content(kind),
        ),
        title='Исследование звукоизоляции ограждающих конструкций',
    )


@router.get(
    '/api/work/forms/{kind}', response_model=FastUI, response_model_exclude_none=True
)
def form_content(kind):
    match kind:
        case 'first':
            return first_form()
