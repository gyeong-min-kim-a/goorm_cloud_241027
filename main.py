import csv
from contextlib import asynccontextmanager
from fastapi import FastAPI

def load_gyul_data():
    with open('./data/gyul.csv', 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        result = { int(row.pop('year')): row for row in reader }
    
    return result
gyul_stats = {}

@asynccontextmanager 
async def lifespan(app: FastAPI):           ## 원래 파이썬은 ducktyping인데, 지금처럼 쓰면 일종의 힌트처럼 쓸 수 있음
    global gyul_stats
    gyul_stats = load_gyul_data()
    
    yield                                   ## 일종의 제너레이터, 이 위는 불러오기 전에 미리 실행하는 것. 데이터를 미리 불러올 경우에 한꺼번에 불러오는게 아니라 하나씩 불러오는 어쩌구
    
app = FastAPI(lifespan = lifespan)
     

@app.get("/")
async def root():
    return {"mesage" : "hello, world"}

@app.get("/stats")
async def gyul_all_stats():
    return gyul_stats

@app.get('/stats/{year}')
async def get_year_stats(year: int):
    return gyul_stats[year]