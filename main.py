import csv
from contextlib import asynccontextmanager
from fastapi import FastAPI


def load_gyul_data():
    with open("./data/gyul.csv", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        result = {int(row.pop("year")): row for row in reader}

    return result


gyul_statistics = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global gyul_statistics
    gyul_statistics = load_gyul_data()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/stats")
async def get_gyul_all_stats():
    return gyul_statistics


@app.get("/stats/{year}")
async def get_gyul_year_stats(year: int):
    return gyul_statistics[year]
