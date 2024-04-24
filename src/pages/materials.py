from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.events import GoToEvent

from src.pages.shared import base_page

router = APIRouter()


@router.get('/materials', response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(
        c.Heading(text='Теоритические материалы', level=2),
        c.Div(
            components=[
                c.Paragraph(text='Лабораторные работы на 2023-2024, яндекс диск:'),
                c.Link(
                    components=[c.Text(text='Ссылка на материалы к работе')],
                    on_click=GoToEvent(
                        url='https://disk.yandex.ru/d/DUkUCWzFp6rhjg', target='_blank'
                    ),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
    )
