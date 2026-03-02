from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.services.groww_search_service import search_option
from app.services.groww_aggregate_service import fetch_latest_aggregated
from pydantic import BaseModel
from typing import Optional
router = APIRouter()


async def handle_search(keyword: str):
    result = await search_option(keyword)

    if not result:
        raise HTTPException(status_code=404, detail="No matching result found")

    return {
        "status": "success",
        "data": result
    }

class SearchOptionRequest(BaseModel):
    keyword: str

# -------------------------------
# GET Version (Query Param)
# -------------------------------

@router.get("/search-option")
async def search_option_query(
    keyword: str = Query(...),
):
    return await handle_search(keyword)


@router.post("/search-option")
async def search_option_post(payload: SearchOptionRequest):
    return await handle_search(payload.keyword)

# -------------------------------
# POST Version (JSON Body)
# -------------------------------



@router.post("/search-option")
async def search_option_body(payload: SearchOptionRequest):
    result = await search_option(payload.keyword)

    if not result:
        raise HTTPException(status_code=404, detail="No matching result found")

    return {
        "status": "success",
        "data": result

    }

@router.get("/latest-aggregated")
async def latest_aggregated():

    result = await fetch_latest_aggregated()

    if not result:
        raise HTTPException(status_code=500, detail="Failed to fetch aggregated data")

    return {
        "status": "success",
        "segment": "CASH",
        "data": result
    }