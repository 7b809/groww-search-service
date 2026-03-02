import httpx
import time
from app.utils.headers_builder import build_headers

BASE_URL = "https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/NIFTY"


async def fetch_index_candles(interval: int = 5, days: int = 5):
    """
    Fetch NIFTY index candles
    """

    end_time = int(time.time() * 1000)
    start_time = end_time - (days * 24 * 60 * 60 * 1000)

    params = {
        "intervalInMinutes": interval,
        "startTimeInMillis": start_time,
        "endTimeInMillis": end_time
    }

    headers = build_headers()

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        return {"candles": []}

    data = response.json()

    candles = []

    for candle in data.get("candles", []):
        candles.append([
            candle[0],  # timestamp
            candle[1],  # open
            candle[2],  # high
            candle[3],  # low
            candle[4],  # close
            candle[5],  # volume
        ])

    return {"candles": candles}