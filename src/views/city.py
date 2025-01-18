from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.common.consts import CommonConsts
from src.modules.services import RealEstateService

router = APIRouter()
templates = Jinja2Templates(directory=CommonConsts.TEMPLATE_PATH)


@router.get("/city", response_class=HTMLResponse)
async def analyze_city(request: Request):
    return templates.TemplateResponse("city.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def analyze_city_post(request: Request, city: str = Form(...)):
    raw_data = RealEstateService.extract()
    tf_data = RealEstateService.transform(raw_data)
    analysis_result = RealEstateService.city_analyze(tf_data, city)
    print(analysis_result)

    return templates.TemplateResponse("city.html", {"request": request, "analysis_result": analysis_result})