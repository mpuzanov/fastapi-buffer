from fastapi import APIRouter, Response, Query
from fastapi import Depends
from typing import List
from typing import Optional

from ..services import BuildingService, FlatService, OccService, PeopleService, PeoplePeriodService
from ..services import CounterService, CounterValueService, ValueService, PayService, DolgService, PdService
from ..services import TipService, FinService, SupService

from ..models import Formats, CommonQueryParams

router = APIRouter(
    prefix='/api',
)


@router.get("/tips", description='Организации', tags=["Таблицы"], summary='Список организаций')
async def get_tips(format: Formats, session: TipService = Depends()):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/finperiods", description='Фин. периоды', tags=["Таблицы"], summary='Список фин. периодов')
async def get_finperiods(format: Formats, session: FinService = Depends()):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/suppliers", description='Поставщики', tags=["Таблицы"],
            summary='Список поставщиков с отдельной квитанцией')
async def get_suppliers(format: Formats, session: SupService = Depends()):
    return Response(content=await session.get_xml(format), media_type=f"application/{format.value}")


@router.get("/buildings", description='Дома', tags=["Выгрузки"], summary="Домов")
async def get_buildings(commons: CommonQueryParams = Depends(CommonQueryParams),
                        session: BuildingService = Depends(),
                        ):
    return Response(content=await session.get_xml(param=commons), media_type=f"application/{commons.format.value}")


@router.get("/flats", description='Помещения', tags=["Выгрузки"], summary="Помещений")
async def get_flats(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: FlatService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/occ", description='Лицевые счета', tags=["Выгрузки"], summary="Лицевых счетов")
async def get_occ(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: OccService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/people", description='Жители', tags=["Выгрузки"], summary="Жителей")
async def get_people(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PeopleService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/people_period", description='Регистрация граждан', tags=["Выгрузки"], summary="Регистрация граждан")
async def get_people_period(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PeoplePeriodService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/counter", description='Счетчики (ПУ)', tags=["Выгрузки"], summary="Приборов учета")
async def get_counter(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: CounterService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/counter_value", description='Показания ПУ', tags=["Выгрузки"], summary="Показаний приборов учета")
async def get_counter_value(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: CounterValueService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/value", description='Начисления', tags=["Выгрузки"], summary="Начислений")
async def get_value(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: ValueService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/pay", description='Оплаты', tags=["Выгрузки"], summary="Оплат")
async def get_pay(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PayService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      sup_id=commons.sup_id, format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/dolg", description='Долги', tags=["Выгрузки"], summary="Долгов")
async def get_dolg(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: DolgService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      sup_id=commons.sup_id, format=commons.format),
        media_type=f"application/{commons.format.value}")


@router.get("/pd", description='Квитанции', tags=["Выгрузки"], summary="Платежных документов")
async def get_pd(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PdService = Depends()
):
    return Response(
        content=await session.get_xml(tip_id=commons.tip_id, build_id=commons.build_id, fin_id=commons.fin_id,
                                      sup_id=commons.sup_id, format=commons.format),
        media_type=f"application/{commons.format.value}")
