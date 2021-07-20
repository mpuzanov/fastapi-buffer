from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from fastapi.responses import FileResponse, StreamingResponse
from ..services.reports import ReportsService
from ..models.common import ServicesPU
from .. import models
from ..services.auth_basic import get_current_user

router = APIRouter(
    prefix='/reports',
    tags=['Отчеты'],
)


@router.get('/export_pu',
            description='Экспорт приборов учета для мобильного приложения',
            summary='Экспорт приборов учета для мобильного приложения',
            response_class=FileResponse)
async def export_xls(
        tip_id: int = Query(..., description="Код организации"),
        build_id: int = Query(None, description="Код дома"),
        fin_id: int = Query(None, description="Код финансового периода"),
        service_id: ServicesPU = Query(None, description="Код услуги"),
        reports_service: ReportsService = Depends(),
        user: models.User = Depends(get_current_user),
):
    params = {"tip_str": tip_id, 'build_id': build_id, 'fin_id': fin_id,
              'service_id': service_id.value if service_id else None}

    output = await reports_service.export_pu_xls(params=params)

    filename = 'export_pu.xls'
    headers = {
        f'Content-Disposition': f'attachment; filename={filename}'
    }

    # Extension  MIME Type
    # .xls application/vnd.ms-excel
    # .xlsx application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

    return StreamingResponse(output, headers=headers, media_type=f"application/vnd.ms-excel")
