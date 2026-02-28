import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.groww_derivative_service import fetch_derivative_data
from app.core.config import settings

router = APIRouter()


@router.websocket("/ws/option/{contract_id}")
async def option_ws(websocket: WebSocket, contract_id: str):
    await websocket.accept()

    try:
        while True:
            data = await fetch_derivative_data(contract_id)

            if data:
                await websocket.send_json(data)

            # Poll every 2 seconds
            await asyncio.sleep(settings.POLL_INTERVAL)

    except WebSocketDisconnect:
        print(f"Client disconnected from {contract_id}")