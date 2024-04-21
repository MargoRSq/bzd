from __future__ import annotations as _annotations

import json
from typing import Literal

from pydantic import TypeAdapter, create_model
from rich import print

from src import data_dir
from src.schemas import FirstElement, SecondVariation

FirstElementsAdapter = TypeAdapter(dict[str, FirstElement])
with open(f'{data_dir}/data_1.json', encoding='UTF-8') as f:
    first_elemets = json.load(f)
    first_data = FirstElementsAdapter.validate_python(first_elemets['data'])

keys = list(first_data.keys())

variations = []
for material, info in first_data.items():
    v = [f'{material} [{tol.name}]' for tol in info.tol]
    variations.extend(v)

# materials = Literal[*keys]

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


SecondElementsAdapter = TypeAdapter(dict[str, SecondVariation])
with open(f'{data_dir}/second.json', encoding='UTF-8') as f:
    second_elements = json.load(f)
    second_data = SecondElementsAdapter.validate_python(second_elements['data'])

# print(second_data)

kinds = Literal[*list(second_data.keys())]
print(kinds, variations)

SecondKChooseModel = create_model(
    'SecondKChooseModel',
    Вид=(kinds, ...),
)
