from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastui import FastUI
from fastui import components as c
from fastui.events import PageEvent

from src.pages.shared import ChooseMaterialModel, base_page

router = APIRouter()


@router.get('/forms/first', response_model=FastUI, response_model_exclude_none=True)
def first_form():
    return [
        c.Heading(text='Введите параметры', level=3, class_name='pb-3'),
        c.ModelForm(
            model=ChooseMaterialModel,
            display_mode='default',
            submit_url='/api/generator/generate_chart',
            method='POST',
        ),
    ]


@router.get('/', response_class=RedirectResponse)
async def redirect_fastapi():
    return '/work/first'


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
