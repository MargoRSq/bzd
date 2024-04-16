import enum

from pydantic import BaseModel, ConfigDict, Field


class ToolEnum(str, enum.Enum):
    kir = 'Кирпичная кладка, оштукатуренная с двух сторон'
    screwdriver = 'screwdriver'
    saw = 'saw'
    claw_hammer = 'claw_hammer'


class Multiplier(str, enum.Enum):
    full = 1
    half = 0.5


class FirstElement(BaseModel):
    id: int
    weight: str = Field(serialization_alias='Вес, кг')
    img_name: str
    d_63: int = Field(validation_alias='63Hz', serialization_alias='63 Гц')
    d_125: int = Field(validation_alias='125Hz', serialization_alias='125 Гц')
    d_250: int = Field(validation_alias='250Hz', serialization_alias='250 Гц')
    d_500: int = Field(validation_alias='500Hz', serialization_alias='500 Гц')
    d_1000: int = Field(validation_alias='1000Hz', serialization_alias='1000 Гц')
    d_2000: int = Field(validation_alias='2000Hz', serialization_alias='2000 Гц')
    d_4000: int = Field(validation_alias='4000Hz', serialization_alias='4000 Гц')
    d_8000: int = Field(validation_alias='8000Hz', serialization_alias='8000 Гц')

    model_config = ConfigDict(coerce_numbers_to_str=True)


class SelectForm(BaseModel):
    material: ToolEnum = Field(title='Вид материала')
    mn: Multiplier = Field(title='Толщина')
