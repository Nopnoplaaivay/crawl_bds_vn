from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.common.consts import CommonConsts
from src.modules.services import RealEstateService

router = APIRouter()
templates = Jinja2Templates(directory=CommonConsts.TEMPLATE_PATH)


@router.get("/city", response_class=HTMLResponse)
async def analyze_city(request: Request):
    analysis_result = RealEstateService.run_pipeline(analysis_method="city")
    return templates.TemplateResponse(
        "city.html", {"request": request, "analysis_result": analysis_result}
    )


@router.post("/", response_class=HTMLResponse)
async def analyze_city_post(request: Request, city: str = Form(...)):
    analysis_result = RealEstateService.run_pipeline(analysis_method="city", city=city)
    return templates.TemplateResponse(
        "city.html", {"request": request, "analysis_result": analysis_result}
    )
