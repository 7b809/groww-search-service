from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.services.groww_search_service import search_option
from app.services.groww_aggregate_service import fetch_latest_aggregated

router = APIRouter()


# -------------------------------
# GET Version (Query Param)
# -------------------------------
@router.get("/search-option")
async def search_option_query(
    keyword: str = Query(...),
    entity_type: Optional[str] = Query(None)
):
    result = await search_option(keyword, entity_type)

    if not result:
        raise HTTPException(status_code=404, detail="No matching result found")

    return {
        "status": "success",
        "data": result
    }


# -------------------------------
# POST Version (JSON Body)
# -------------------------------
class SearchRequest(BaseModel):
    keyword: str
    entity_type: Optional[str] = None


@router.post("/search-option")
async def search_option_body(payload: SearchRequest):
    result = await search_option(payload.keyword, payload.entity_type)

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