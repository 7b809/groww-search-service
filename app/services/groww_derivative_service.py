import httpx
from app.utils.headers_builder import build_headers
from app.core.config import settings

BASE_URL = settings.GROWW_DERIVATIVE_BASE_URL

async def fetch_derivative_data(contract_id: str):

    params = {
        "groww_contract_id": contract_id
    }

    headers = build_headers()

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(BASE_URL, params=params, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    live = data.get("livePrice", {})
    contract = data.get("contractDetails", {})

    # ✅ Filter only required OHLCV + Option data
    return {
        "symbol": live.get("symbol"),
        "timestamp": live.get("tsInMillis"),
        "open": live.get("open"),
        "high": live.get("high"),
        "low": live.get("low"),
        "close": live.get("close"),
        "ltp": live.get("ltp"),
        "volume": live.get("volume"),
        "open_interest": live.get("openInterest"),
        "oi_change": live.get("oiDayChange"),
        "oi_change_perc": live.get("oiDayChangePerc"),

        "option_type": contract.get("optionType"),
        "expiry": contract.get("expiry"),
        "lot_size": contract.get("lotSize"),
        "contract_id": contract.get("growwContractId")
    }