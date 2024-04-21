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
from src.pages.shared import ChooseMaterialModel, first_data, tols_dict
from src.schemas import FirstVariation

router = APIRouter()


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
