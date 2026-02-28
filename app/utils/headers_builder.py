# app/utils/headers_builder.py

import uuid

def build_headers():
    return {
        "accept": "application/json, text/plain, */*",
        "x-app-id": "growwWeb",
        "x-device-type": "charts",
        "x-platform": "web"
    }