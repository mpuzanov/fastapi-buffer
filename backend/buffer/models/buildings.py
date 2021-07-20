from typing import Optional

from pydantic import BaseModel


class Building(BaseModel):
    UID_Doma: str
    Gorod: str
    Ulitsya: str
    Nomer_Doma: str
    Korpus: str
    Tip_Doma: str
    Kolichestvo_podyezdov: Optional[int]
    Kolichestvo_etagei: Optional[int]
    Obshaya_Ploshad: str
    Zhilaya_Ploshad: str
    Komm_Ploshad: str
