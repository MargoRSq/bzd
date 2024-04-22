import re
from typing import Annotated

import numpy as np
from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup
from fastui.forms import fastui_form
from matplotlib import pyplot as plt

from src import static_dir
from src.pages.shared import centered_div
from src.pages.work import ThirdForm
from src.parser import (
    ChooseMaterialModel,
    SecondKChooseModel,
    objects_dict,
    second_data,
    tols_dict,
)
from src.schemas import FirstVariation, HZVaritation, HZVaritationFloats

router = APIRouter()


@router.post('/generate_chart', response_model=FastUI, response_model_exclude_none=True)
async def generate_image(
    form: Annotated[ChooseMaterialModel, fastui_form(ChooseMaterialModel)],
):
    sp = form.Материал.split('[')
    material, tol = sp[0][:-1], sp[1][:-1]
    element = tols_dict[material][tol]
    generate_first_image(form.Материал, element)

    return [
        c.Heading(text=form.Материал, level=3, class_name='pb-3'),
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
        centered_div(c.Image(src=f'/static/{form.Материал}.png')),
    ]


@router.post('/generate_graph', response_model=FastUI, response_model_exclude_none=True)
async def generate_graph(
    form: Annotated[SecondKChooseModel, fastui_form(SecondKChooseModel)],
):
    element = second_data[form.Вид]
    main_hz = HZVaritation(
        weight=element.weight,
        d_63=element.d_63,
        d_125=element.d_125,
        d_250=element.d_250,
        d_500=element.d_500,
        d_1000=element.d_1000,
        d_2000=element.d_2000,
        d_4000=element.d_4000,
        d_8000=element.d_8000,
    )
    shum_hz = HZVaritation(
        weight=element.weight,
        d_63=element.d_63_shum,
        d_125=element.d_125_shum,
        d_250=element.d_250_shum,
        d_500=element.d_500_shum,
        d_1000=element.d_1000_shum,
        d_2000=element.d_2000_shum,
        d_4000=element.d_4000_shum,
        d_8000=element.d_8000_shum,
    )
    generate_second_image(form.Вид, main_hz, shum_hz)

    return [
        c.Heading(text=form.Вид, level=3, class_name='mt-3'),
        c.Table(
            data=[main_hz],
            columns=[DisplayLookup(field='Кг/м2', title='кг/м2')],
        ),
        centered_div(
            c.Heading(
                text='Среднегеометрические частоты октавных полос',
                level=2,
                class_name='mb-3',
            )
        ),
        c.Div(
            components=[
                c.Heading(text='L шумн (шумное помещение)', level=3),
                c.Table(
                    data=[main_hz],
                    columns=[
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
            ]
        ),
        c.Div(
            components=[
                c.Heading(text='L допустимое (тихое помещение)', level=3),
                c.Table(
                    data=[shum_hz],
                    columns=[
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
            ]
        ),
        centered_div(c.Image(src=f'/static/{form.Вид}.png', width='50%')),
    ]


@router.post('/generate_table', response_model=FastUI, response_model_exclude_none=True)
async def generate_table(
    form: Annotated[ThirdForm, fastui_form(ThirdForm)],
):
    sp = form.конструкция.тип.split('[')
    object, uplot = sp[0][:-1], sp[1][:-1]
    input_table = objects_dict[object][uplot]
    output = generate_third_table(input_table, form)
    return [
        c.Heading(text=form.конструкция.тип, level=3),
        c.Table(
            data=[form],
            columns=[
                DisplayLookup(field='S'),
                DisplayLookup(field='Lp [от 85 до 120]', title='Lp'),
                DisplayLookup(field='r [от 1 до 10]', title='r'),
                DisplayLookup(field='alpha', title='α'),
            ],
        ),
        c.Heading(text='Lдоп (допустимое)', level=3, class_name='pt-3'),
        c.Table(
            data=[output],
            columns=[
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
        c.Heading(text='Lзи треб (требуемая звукоизоляция)', level=3),
        c.Table(
            data=[output],
            columns=[
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
    ]


def generate_first_image(name, tol: FirstVariation):
    number_pattern = re.search(r'[-+]?[0-9]*\.?[0-9]+', tol.name)
    number = float(number_pattern.group())
    y_axis = [13.8 * np.log10(x) * tol.weight * number for x in tol.x_axis]
    plt.figure()
    plt.plot(tol.x_axis, y_axis, label='ЗИ = 13.8 * lg(m)')
    plt.title(name)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.legend()

    path = f'{static_dir}/{name}.png'
    with open(path, mode='w') as f:
        f.write('1')
    plt.savefig(path)
    plt.close()


def generate_second_image(name, main_hz: HZVaritation, shum: HZVaritation):
    plt.figure()
    x_axis = main_hz.key_hzs
    y_axis = np.array(shum.value_hzs) - np.array(main_hz.value_hzs)
    print(y_axis)
    plt.plot(range(len(x_axis)), y_axis, marker='o', label='dL, Lшумн - Lдоп')

    plt.xticks(range(len(x_axis)), x_axis)
    plt.yticks(y_axis)
    plt.grid(True)
    plt.legend()

    path = f'{static_dir}/{name}.png'
    with open(path, mode='w') as f:
        f.write('1')
    plt.savefig(path)
    plt.close()


def generate_third_table(input_data, form_data: ThirdForm):
    at = float(form_data.alpha)
    b = (at * form_data.s) * (1 - at)
    lshum = form_data.lp - 20 * np.log10(form_data.r) - 20 * np.log10(b) + 6
    return HZVaritationFloats(
        d_63=lshum - input_data.d_63,
        d_125=lshum - input_data.d_125,
        d_250=lshum - input_data.d_250,
        d_500=lshum - input_data.d_500,
        d_1000=lshum - input_data.d_1000,
        d_2000=lshum - input_data.d_2000,
        d_4000=lshum - input_data.d_4000,
        d_8000=lshum - input_data.d_8000,
    )
