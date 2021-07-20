from fastapi import APIRouter, Response
from fastapi import Depends

from ..services import BuildingService, FlatService, OccService, PeopleService, PeoplePeriodService
from ..services import CounterService, CounterValueService, ValueService, PayService, DolgService, PdService

from ..models import CommonQueryParams
from .. import models
from ..services.auth_basic import get_current_user

router = APIRouter(
    prefix='/api',
    tags=['Выгрузки'],
)


@router.get("/buildings", description='Дома', tags=["Выгрузки"], summary="Домов")
async def get_buildings(commons: CommonQueryParams = Depends(CommonQueryParams),
                        session: BuildingService = Depends(),
                        user: models.User = Depends(get_current_user),
                        ):
    return Response(content=await session.get_xml(param=commons), media_type=f"application/{commons.format.value}")


@router.get("/flats", description='Помещения', tags=["Выгрузки"], summary="Помещений")
async def get_flats(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: FlatService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/occ", description='Лицевые счета', tags=["Выгрузки"], summary="Лицевых счетов")
async def get_occ(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: OccService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/people", description='Жители', tags=["Выгрузки"], summary="Жителей")
async def get_people(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PeopleService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/people_period", description='Регистрация граждан', tags=["Выгрузки"], summary="Регистрация граждан")
async def get_people_period(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PeoplePeriodService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/counter", description='Счетчики (ПУ)', tags=["Выгрузки"], summary="Приборов учета")
async def get_counter(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: CounterService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/counter_value", description='Показания ПУ', tags=["Выгрузки"], summary="Показаний приборов учета")
async def get_counter_value(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: CounterValueService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/value", description='Начисления', tags=["Выгрузки"], summary="Начислений")
async def get_value(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: ValueService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/pay", description='Оплаты', tags=["Выгрузки"], summary="Оплат")
async def get_pay(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PayService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/dolg", description='Долги', tags=["Выгрузки"], summary="Долгов")
async def get_dolg(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: DolgService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")


@router.get("/pd", description='Квитанции', tags=["Выгрузки"], summary="Платежных документов")
async def get_pd(
        commons: CommonQueryParams = Depends(CommonQueryParams),
        session: PdService = Depends(),
        user: models.User = Depends(get_current_user),
):
    return Response(
        content=await session.get_xml(**commons.get_dict_params()),
        media_type=f"application/{commons.format.value}")
