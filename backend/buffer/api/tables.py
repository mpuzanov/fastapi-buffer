from fastapi import APIRouter, Response
from fastapi import Depends

from ..services import TipService, FinService, SupService, TownService, StreetService
from ..models import Formats
from .. import models
from ..services.auth_basic import get_current_user

router = APIRouter(
    prefix='/api',
    tags=['Таблицы'],
)


@router.get("/tips",
            description='Организации',
            tags=["Таблицы"],
            summary='Список организаций')
async def get_tips(format: Formats = Formats.xml,
                   session: TipService = Depends(),
                   user: models.User = Depends(get_current_user),
                   ):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/finperiods",
            description='Фин. периоды',
            tags=["Таблицы"],
            summary='Список фин. периодов')
async def get_finperiods(format: Formats = Formats.xml,
                         session: FinService = Depends(),
                         user: models.User = Depends(get_current_user),
                         ):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/suppliers",
            description='Поставщики',
            tags=["Таблицы"],
            summary='Список поставщиков с отдельной квитанцией')
async def get_suppliers(format: Formats = Formats.xml,
                        session: SupService = Depends(),
                        user: models.User = Depends(get_current_user),
                        ):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/towns",
            description='Населённые пункты',
            tags=["Таблицы"],
            summary='Список населённых пунктов')
async def get_streets(format: Formats = Formats.xml,
                      session: TownService = Depends(),
                      user: models.User = Depends(get_current_user),
                      ):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/streets",
            description='Улицы',
            tags=["Таблицы"],
            summary='Список улиц')
async def get_streets(town_id: int = 1,
                      format: Formats = Formats.xml,
                      session: StreetService = Depends(),
                      user: models.User = Depends(get_current_user),
                      ):
    return Response(content=await session.get_xml(town_id, format), media_type=f"application/{format.value}")
