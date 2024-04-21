import enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ToolEnum(str, enum.Enum):
    kir = 'Кирпичная кладка, оштукатуренная с двух сторон'
    screwdriver = 'screwdriver'
    saw = 'saw'
    claw_hammer = 'claw_hammer'


def create_dynamic_literal(*values):
    """Создает тип Literal динамически."""
    return Literal[*values]
    # return Enum(name, enum_dict)


class Multiplier(str, enum.Enum):
    full = 1
    half = 0.5


class FirstVariation(BaseModel):
    name: str
    weight: float = Field(default=1, serialization_alias='Вес, кг')
    d_63: int = Field(validation_alias='63Hz', serialization_alias='63 Гц')
    d_125: int = Field(validation_alias='125Hz', serialization_alias='125 Гц')
    d_250: int = Field(validation_alias='250Hz', serialization_alias='250 Гц')
    d_500: int = Field(validation_alias='500Hz', serialization_alias='500 Гц')
    d_1000: int = Field(validation_alias='1000Hz', serialization_alias='1000 Гц')
    d_2000: int = Field(validation_alias='2000Hz', serialization_alias='2000 Гц')
    d_4000: int = Field(validation_alias='4000Hz', serialization_alias='4000 Гц')
    d_8000: int = Field(validation_alias='8000Hz', serialization_alias='8000 Гц')

    @computed_field
    @property
    def x_axis(self) -> list[int]:
        return [
            self.d_63,
            self.d_125,
            self.d_250,
            self.d_500,
            self.d_1000,
            self.d_2000,
            self.d_4000,
            self.d_8000,
        ]


class FirstElement(BaseModel):
    img_name: str
    tol: list[FirstVariation]

    model_config = ConfigDict(coerce_numbers_to_str=True)


class SecondVariation(BaseModel):
    # name: str
    weight: float = Field(default=1, serialization_alias='Кг/м2')
    d_63: int = Field(validation_alias='63Hz_dop', serialization_alias='63 Гц')
    d_125: int = Field(validation_alias='125Hz_dop', serialization_alias='125 Гц')
    d_250: int = Field(validation_alias='250Hz_dop', serialization_alias='250 Гц')
    d_500: int = Field(validation_alias='500Hz_dop', serialization_alias='500 Гц')
    d_1000: int = Field(validation_alias='1000Hz_dop', serialization_alias='1000 Гц')
    d_2000: int = Field(validation_alias='2000Hz_dop', serialization_alias='2000 Гц')
    d_4000: int = Field(validation_alias='4000Hz_dop', serialization_alias='4000 Гц')
    d_8000: int = Field(validation_alias='8000Hz_dop', serialization_alias='8000 Гц')
    d_63_shum: int = Field(validation_alias='63Hz_shumn', serialization_alias='63 Гц')
    d_125_shum: int = Field(
        validation_alias='125Hz_shumn', serialization_alias='125 Гц'
    )
    d_250_shum: int = Field(
        validation_alias='250Hz_shumn', serialization_alias='250 Гц'
    )
    d_500_shum: int = Field(
        validation_alias='500Hz_shumn', serialization_alias='500 Гц'
    )
    d_1000_shum: int = Field(
        validation_alias='1000Hz_shumn', serialization_alias='1000 Гц'
    )
    d_2000_shum: int = Field(
        validation_alias='2000Hz_shumn', serialization_alias='2000 Гц'
    )
    d_4000_shum: int = Field(
        validation_alias='4000Hz_shumn', serialization_alias='4000 Гц'
    )
    d_8000_shum: int = Field(
        validation_alias='8000Hz_shumn', serialization_alias='8000 Гц'
    )

    @computed_field
    @property
    def x_axis(self) -> list[int]:
        return [
            self.d_63,
            self.d_125,
            self.d_250,
            self.d_500,
            self.d_1000,
            self.d_2000,
            self.d_4000,
            self.d_8000,
        ]

    @computed_field
    @property
    def x_axis_shum(self) -> list[int]:
        return [
            self.d_63_shum,
            self.d_125_shum,
            self.d_250_shum,
            self.d_500_shum,
            self.d_1000_shum,
            self.d_2000_shum,
            self.d_4000_shum,
            self.d_8000_shum,
        ]


class HZVaritation(BaseModel):
    weight: float = Field(default=1, serialization_alias='Кг/м2')
    d_63: int = Field(serialization_alias='63 Гц')
    d_125: int = Field(serialization_alias='125 Гц')
    d_250: int = Field(serialization_alias='250 Гц')
    d_500: int = Field(serialization_alias='500 Гц')
    d_1000: int = Field(serialization_alias='1000 Гц')
    d_2000: int = Field(serialization_alias='2000 Гц')
    d_4000: int = Field(serialization_alias='4000 Гц')
    d_8000: int = Field(serialization_alias='8000 Гц')

    @computed_field
    @property
    def value_hzs(self) -> list[int]:
        return [
            self.d_63,
            self.d_125,
            self.d_250,
            self.d_500,
            self.d_1000,
            self.d_2000,
            self.d_4000,
            self.d_8000,
        ]

    @computed_field
    @property
    def key_hzs(self) -> list[int]:
        return [63, 125, 250, 500, 1000, 2000, 4000, 8000]
