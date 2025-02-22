import os
from typing import Annotated, Literal, Optional, Union
from datetime import datetime, timedelta

from loguru import logger

import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, ConfigDict

from src.scheduler.search_papers import DateRangeSearchClient

app = FastAPI()

today = datetime.now().strftime("%Y%m%d")
start_required = Annotated[Optional[str],Field(today, ge="20250222", le=today)]
end_required = Annotated[Optional[str], Field(today, ge="20250222", le=today)]
    
class FilterParams(BaseModel):
    scope: Literal["range", "latest"] = "latest"
    start: start_required
    end: end_required
    topn: int = 10
    sortby: Literal["author-cited", "paper-cited", "date"] = "author-cited"

@app.get("/")
def read_root():
    week_today = datetime.now().strftime("%Y%W")
    return {"Hello": week_today}

@app.post("/items")
def get_item(param: FilterParams):
    sort_field = {
        "author-cited": "citation_author",
        "paper-cited": "citation_paper",
        "date": "published"
    }
    filter_outfield = ["id", "title", "summary", "author", "published", "citation_author", "citation_paper"]
    
    if param.scope == "latest":
        dirs = os.listdir("./output/weekly")
        data_file = sorted([f"./output/weekly/{d}" for d in dirs if d.endswith(".csv")])[0]
    logger.debug(f"dirs: {data_file}")
    
    df_data = pd.read_csv(data_file)
    df_data_sorted = df_data.sort_values(by=sort_field[param.sortby], ascending=False)
    df_data_filtered = df_data_sorted[filter_outfield][:param.topn]
    logger.debug(f"dirs: {df_data_filtered}")
    
    return {"datas": df_data_filtered.to_dict(orient="records")}

@app.get("/execute/{span}")
def read_item(span: str):
    client = DateRangeSearchClient()
    if span == "weekly":
        client.search_weekly()
        week_today = datetime.now().strftime("%Y%W")
        client.search_results_to_csv(f"doc/output/weekly/{week_today}.csv")