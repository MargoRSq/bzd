import json
import os
from typing import Annotated

from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup
from fastui.forms import fastui_form
from matplotlib import pyplot as plt
from pydantic import TypeAdapter

from src.schemas import FirstElement, SelectForm

router = APIRouter()

