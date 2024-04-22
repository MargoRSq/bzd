from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastui import FastUI
from fastui import components as c
from fastui.events import PageEvent
from pydantic import BaseModel, Field

from src.pages.shared import base_page, centered_div
from src.parser import ChooseMaterialModel, SecondKChooseModel, ThirdChooseModel

router = APIRouter()


@router.get('/forms/first', response_model=FastUI, response_model_exclude_none=True)
def first_form():
    return [
        c.Heading(
            text='Звукоизолирующая способность стен и перегородок акустичких конструкций и перекрытий',
            level=3,
            class_name='pb-3',
        ),
        centered_div(c.Image(src='/static/kir.png')),
        # c.Heading(text='Вид материала:', level=3, class_name='pb-3'),
        c.ModelForm(
            model=ChooseMaterialModel,
            display_mode='default',
            submit_url='/api/generator/generate_chart',
            method='POST',
        ),
    ]


@router.get('/forms/second', response_model=FastUI, response_model_exclude_none=True)
def second_form():
    return [
        c.Heading(
            text='Допустимые уровни шума на рабочих частотах',
            level=3,
            class_name='pb-3',
        ),
        centered_div(c.Image(src='/static/komn.png')),
        centered_div(
            c.Heading(
                text='Вид трудовой деятельности',
                level=3,
                class_name='border-bottom pt-3 pb-1 mb-3',
            )
        ),
        c.ModelForm(
            model=SecondKChooseModel,
            display_mode='default',
            submit_url='/api/generator/generate_graph',
            method='POST',
        ),
    ]


class ThirdForm(BaseModel):
    s: float = Field(default=1, alias='S')
    lp: int = Field(default=85, alias='Lp [от 85 до 120]', ge=85, le=120)
    r: int = Field(default=1, alias='r [от 1 до 10]', ge=1, le=10)
    alpha: str = Field(
        default='0.1', 
    )
    конструкция: ThirdChooseModel


@router.get('/forms/third', response_model=FastUI, response_model_exclude_none=True)
def third_form():
    return [
        c.Heading(
            text='Звукоизолирующая способность дверей и окон, Дб',
            level=3,
            class_name='pb-3',
        ),
        c.Div(
            components=[
                c.Image(src='/static/third_formulas.png', width='50%'),
                c.Image(src='/static/third.png', width='50%'),
            ]
        ),
        c.ModelForm(
            model=ThirdForm,
            display_mode='default',
            submit_url='/api/generator/generate_table',
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
        case 'second':
            return second_form()
        case 'third':
            return third_form()
