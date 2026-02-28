import httpx
from app.utils.headers_builder import build_headers
from app.core.config import settings

BASE_URL = settings.GROWW_SEARCH_BASE_URL

async def search_option(keyword: str, entity_type: str | None = None):

    params = {
        "page": 0,
        "query": keyword,
        "size": 15,
        "web": "true"
    }

    # Optional entity_type
    if entity_type:
        params["entity_type"] = entity_type

    headers = build_headers()

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            BASE_URL,
            params=params,
            headers=headers
        )

    if response.status_code != 200:
        return None

    data = response.json()
    content = data.get("data", {}).get("content", [])

    if not content:
        return None

    return content[0]   # return first match