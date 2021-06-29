import uvicorn
from fastapi import FastAPI

from .config import settings

app = FastAPI(
    title='API выгрузки информации в Буфер ИВЦ',
    description='',
    version='1.0.0.0',
    debug=settings.debug,
    root_path=settings.root_path,    
)

if __name__ == '__main__':
    uvicorn.run(
        'web:app',
        reload=settings.autoreload,
        host=settings.service_host,
        port=settings.service_port,
        log_level=settings.log_level.lower(),
    )
