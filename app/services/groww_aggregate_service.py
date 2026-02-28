import httpx
from app.utils.headers_builder import build_headers
from app.core.config import settings

BASE_URL = settings.GROWW_AGGREGATED_BASE_URL

async def fetch_latest_aggregated():

    headers = build_headers()
    headers["content-type"] = "application/json"

    payload = {
        "exchangeAggReqMap": {
            "NSE": {
                "priceSymbolList": [],
                "indexSymbolList": [
                    "NIFTY",
                    "BANKNIFTY",
                    "FINNIFTY",
                    "NIFTYMIDSELECT"
                ]
            },
            "BSE": {
                "priceSymbolList": [],
                "indexSymbolList": [
                    "SENSEX",
                    "14"
                ]
            }
        }
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            BASE_URL,
            json=payload,
            headers=headers
        )

    if response.status_code != 200:
        return None

    data = response.json()

    result = []

    exchange_map = data.get("exchangeAggRespMap", {})

    for exchange, exchange_data in exchange_map.items():
        index_map = exchange_data.get("indexLivePointsMap", {})

        for symbol, values in index_map.items():
            result.append({
                "exchange": exchange,
                "symbol": symbol,
                "timestamp": values.get("tsInMillis"),
                "open": values.get("open"),
                "high": values.get("high"),
                "low": values.get("low"),
                "close": values.get("close"),
                "value": values.get("value"),
                "day_change": values.get("dayChange"),
                "day_change_perc": values.get("dayChangePerc"),
            })

    return result