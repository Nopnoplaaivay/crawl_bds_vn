from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.common.consts import CommonConsts
from src.modules.services import RealEstateService


router = APIRouter()
templates = Jinja2Templates(directory=CommonConsts.TEMPLATE_PATH)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    RealEstateService.run_pipeline(analysis_method="overview")
    return templates.TemplateResponse("overview.html", {"request": request})