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
from src.pages.work import ThirdForm
from src.parser import (
    ChooseMaterialModel,
    SecondKChooseModel,
    first_data,
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
    sp = form.material.split('[')
    material, tol = sp[0][:-1], sp[1][:-1]
    print(material, tol)
    element = first_data[material].tol[0]
    element = tols_dict[material][tol]
    mat_element = first_data[material]
    generate_first_image(form.material, element)

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
                    src=f'/static/{mat_element.img_name}',
                    width='50%',
                ),
                c.Image(src=f'/static/{form.material}.png', width='50%'),
            ],
        ),
        # c.Button(
        #     text='Обратно',
        #     on_click=PageEvent(
        #         name='change-form', context={'kind': 'first'}, clear=True
        #     ),
        # ),
        # c.Div(
        #     components=[],
        #     class_name='d-flex justify-content-center pt-3 ',
        # ),
    ]


@router.post('/generate_graph', response_model=FastUI, response_model_exclude_none=True)
async def generate_graph(
    form: Annotated[SecondKChooseModel, fastui_form(SecondKChooseModel)],
):
    # sp = form.material.split('[')
    # material, tol = sp[0][:-1], sp[1][:-1]
    # print(material, tol)
    # element = first_data[material].tol[0]
    # element = tols_dict[material][tol]
    # mat_element = first_data[material]

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
            columns=[DisplayLookup(field='Кг/м2', title='Отношение Кг/м2')],
        ),
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
        c.Div(
            components=[
                c.Image(
                    src='/static/komn.png',
                    width='50%',
                ),
                c.Image(src=f'/static/{form.Вид}.png', width='50%'),
            ],
        ),
        # c.Button(
        #     text='Обратно',
        #     on_click=PageEvent(
        #         name='change-form', context={'kind': 'first'}, clear=True
        #     ),
        # ),
        # c.Div(
        #     components=[],
        #     class_name='d-flex justify-content-center pt-3 ',
        # ),
    ]


@router.post('/generate_table', response_model=FastUI, response_model_exclude_none=True)
async def generate_table(
    form: Annotated[ThirdForm, fastui_form(ThirdForm)],
):
    print(form)
    sp = form.конструкция.тип.split('[')
    object, uplot = sp[0][:-1], sp[1][:-1]
    print(object, uplot)
    input_table = objects_dict[object][uplot]
    output = generate_third_table(input_table, form)
    return [
        c.Heading(text=form.конструкция.тип, level=2),
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
    print(name, tol)
    number_pattern = re.search(r'[-+]?[0-9]*\.?[0-9]+', tol.name)
    number = float(number_pattern.group())
    y_axis = [13.8 * np.log10(x) * tol.weight * number for x in tol.x_axis]
    plt.figure()
    plt.plot(tol.x_axis, y_axis, label='Sample Data')
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
    plt.plot(range(len(x_axis)), y_axis, marker='o')

    plt.xticks(range(len(x_axis)), x_axis)
    plt.yticks(y_axis)
    # plt.plot(x_axis, y_axis, label='Sample Data')
    plt.grid(True)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.legend()

    path = f'{static_dir}/{name}.png'
    with open(path, mode='w') as f:
        f.write('1')
    plt.savefig(path)
    plt.close()


def generate_third_table(input_data, form_data: ThirdForm):
    at = float(form_data.at)
    b = (at * form_data.ssum) * (1 - at)
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
