
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from black_friday.constants import APP_HOST, APP_PORT
from black_friday.pipeline.prediction_pipeline import BlackFridayData, BlackFridayPredictor
from black_friday.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.gender: Optional[str] = None
        self.age: Optional[str] = None
        self.occupation: Optional[str] = None
        self.city_category: Optional[str] = None
        self.stay_in_current_city_years: Optional[str] = None
        self.marital_status: Optional[str] = None
        self.product_category_1: Optional[str] = None
        self.product_category_2: Optional[str] = None
        self.product_category_3: Optional[str] = None
        

    async def get_blackfriday_data(self):
        form = await self.request.form()

        self.gender = form.get("gender")
        self.age = form.get("age")
        self.occupation = form.get("occupation")
        self.city_category = form.get("city_category")
        self.stay_in_current_city_years = form.get("stay_in_current_city_years")
        self.marital_status = form.get("marital_status")
        self.product_category_1 = form.get("product_category_1")
        self.product_category_2 = form.get("product_category_2")
        self.product_category_3 = form.get("product_category_3")


@app.get("/", tags=["authentication"])
async def index(request: Request):

    return templates.TemplateResponse(
            "blackfriday.html",{"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_blackfriday_data()
        
        blackfriday_data = BlackFridayData(
                                gender = form.gender,
                                age = form.age,
                                occupation = form.occupation,
                                city_category = form.city_category,
                                stay_in_current_city_years = form.stay_in_current_city_years,
                                marital_status = form.marital_status,
                                product_category_1 = form.product_category_1,
                                product_category_2 = form.product_category_2,
                                product_category_3 = form.product_category_3,

                                )
        


        blackfriday_df = blackfriday_data.get_blackfriday_input_data_frame()

        model_predictor = BlackFridayPredictor()

        value = model_predictor.predict(dataframe=blackfriday_df)[0]

        # status = None
        # if value == 1:
        #     status = "Visa-approved"
        # else:
        #     status = "Visa Not-Approved"

        return templates.TemplateResponse(
            "blackfriday.html",
            {"request": request, "context": value},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

